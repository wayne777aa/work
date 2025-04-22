// 112550020

`include "ProgramCounter.v"
`include "Instr_Memory.v"
`include "Reg_File.v"
`include "Data_Memory.v"
`include "Decoder.v"
`include "ALU.v"
`include "ALU_Ctrl.v"
`include "Sign_Extend.v"
`include "Shift_Left_Two_32.v"
// `include "MUX_2to1.v"
`include "MUX_3to1.v"
`include "Adder.v"

module Simple_Single_CPU(
    clk_i,
	rst_i
);
		
// I/O port
input         clk_i;
input         rst_i;

// Internal Signals
wire [31:0] pc_cur, pc_plus_4, pc_next, pc_mux_result, instr, branch_destination, branch_result;
wire [31:0] RSdata, RTdata, write_data;
wire [4:0] RSaddr, RDaddr;
wire alu_zero, alu_overflow;
wire [31:0] immediate, alu_src2, alu_result, mem_data, branch_addr;
wire [3:0] ALUCtrl;
wire [31:0] immsl2;
wire branch_select;

// control signal
wire [1:0] ALUOp;
wire [1:0] RegDst, MemtoReg, Branch;
wire RegWrite, ALUSrc, Jump, MemRead, MemWrite, jr;

// Components

assign pc_plus_4 = pc_cur + 4;
ProgramCounter PC(
    .clk_i(clk_i),      
    .rst_i(rst_i),     
    .pc_in_i(pc_next),
    .pc_out_o(pc_cur)
);

Instr_Memory IM(
    .pc_addr_i(pc_cur),  
    .instr_o(instr)
);

assign jr = ((instr[31:26] == 6'b000000) && (instr[5:0]) == 6'b001000)? 1: 0;

// if jr => need $ra data => get it by rsdata
MUX_2to1 #(.size(5)) RSaddr_mux(
    .data0_i(instr[25:21]),
    .data1_i(5'b11111),
    .select_i(jr),
    .data_o(RSaddr)
);

Reg_File Registers(
    .clk_i(clk_i),
    .rst_i(rst_i),
    .RSaddr_i(RSaddr),
    .RTaddr_i(instr[20:16]),
    .RDaddr_i(RDaddr), 
    .RDdata_i(write_data),
    .RegWrite_i(RegWrite),
    .RSdata_o(RSdata),  
    .RTdata_o(RTdata) 
);
	
Data_Memory Data_Memory(
	.clk_i(clk_i),
	.addr_i(alu_result), 
	.data_i(RTdata), 
	.MemRead_i(MemRead), 
	.MemWrite_i(MemWrite), 
	.data_o(mem_data)
);

Decoder decoder(
	.instr_op_i(instr[31:26]),
	.ALU_op_o(ALUOp),
	.ALUSrc_o(ALUSrc),
	.RegWrite_o(RegWrite),
	.RegDst_o(RegDst),
	.Branch_o(Branch),
	.Jump_o(Jump),
	.MemRead_o(MemRead),
	.MemWrite_o(MemWrite),
	.MemtoReg_o(MemtoReg)
);

//rt, rd, $ra
MUX_3to1 #(.size(5)) write_data_mux(
    .data0_i(instr[20:16]),
    .data1_i(instr[15:11]),
    .data2_i(5'b11111),
    .select_i(RegDst), // 2: $ra
    .data_o(RDaddr)
);

MUX_2to1 #(.size(32)) alu_src_mux(
    .data0_i(RTdata),
    .data1_i(immediate),
    .select_i(ALUSrc),
    .data_o(alu_src2)
);

ALU_Ctrl alu_ctrl(
    .funct_i(instr[5:0]),
    .ALUOp_i(ALUOp),
    .ALUCtrl_o(ALUCtrl)
);

ALU alu(
    .src1_i(RSdata),
    .src2_i(alu_src2),
    .shamt_i(instr[10:6]),
    .ctrl_i(ALUCtrl),
    .result_o(alu_result),
    .zero_o(alu_zero),
    .overflow(alu_overflow)
);

Sign_Extend sign_extend(
    .data_i(instr[15:0]),
    .data_o(immediate)
);

Shift_Left_Two_32 sl2(
    .data_i(immediate),
    .data_o(immsl2)
);

Adder adder(
    .src1_i(pc_plus_4),
	.src2_i(immsl2),
	.sum_o(branch_destination)
);

MUX_3to1 #(.size(32)) memtoreg_mux(
    .data0_i(alu_result),
    .data1_i(mem_data),
    .data2_i(pc_plus_4),
    .select_i(MemtoReg), // 2: PC+4
    .data_o(write_data)
);

// 1:beq 2:bne
assign branch_select = ((Branch == 2'b01 && alu_zero) || (Branch == 2'b10 && ~alu_zero))? 1 : 0;

MUX_2to1 #(.size(32)) beq_mux(
    .data0_i(pc_plus_4),
    .data1_i(branch_destination),
    .select_i(branch_select),
    .data_o(branch_result)
);

//branch, jump
MUX_2to1 #(.size(32)) pc_src_mux1(
    .data0_i(branch_result),
    .data1_i({pc_plus_4[31:28], instr[25:0], 2'b00}),
    .select_i(Jump),
    .data_o(pc_mux_result)
);

//above result, $ra(jr)
MUX_2to1 #(.size(32)) pc_src_mux2(
    .data0_i(pc_mux_result),
    .data1_i(RSdata),
    .select_i(jr),
    .data_o(pc_next)
);

endmodule