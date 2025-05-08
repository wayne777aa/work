// 112550020

`include "Adder.v"
`include "ALU_Ctrl.v"
`include "ALU.v"
`include "Reg_File.v"
`include "Data_Memory.v"
`include "Decoder.v"
`include "Instruction_Memory.v"
// `include "MUX_2to1.v"
`include "MUX_3to1.v"
`include "Pipe_Reg.v"
`include "ProgramCounter.v"
`include "Shift_Left_Two_32.v"
`include "Sign_Extend.v"

`timescale 1ns / 1ps

module Pipe_CPU(
    clk_i,
    rst_i
    );

input clk_i;
input rst_i;

// TO DO
//--Internal signal-------------------------------------------------------------------------------------------------- 
// IF stage
wire [31:0] pc_cur, pc_plus_4, pc_next, instr, branch_result;

// ID stage
wire [31:0] RSdata, RTdata, immediate;
wire [4:0] RDaddr;
wire [1:0] ALUOp;
wire [1:0] RegDst, MemtoReg, Branch;
wire ALUSrc, RegWrite, Jump, MemRead, MemWrite;

//pipe
wire [31:0] instr_1, pc_plus_4_1;

// EX stage
wire [31:0] branch_destination, alu_src2, alu_result;
wire [3:0] ALUCtrl;
wire alu_zero, alu_overflow;
wire [31:0] immsl2;
wire [4:0] write_address;

//pipe
wire [31:0] instr_2, pc_plus_4_2, RSdata_2, RTdata_2, immediate_2;
wire [4:0] write_addr_RT, write_addr_RD;
wire [1:0] ALUOp_2;
wire [1:0] RegDst_2, MemtoReg_2, Branch_2;
wire ALUSrc_2, RegWrite_2, MemRead_2, MemWrite_2;

// MEM stage
wire [31:0] mem_data;
wire branch_select;

//pipe
wire [31:0] branch_destination_3, alu_result_3, RTdata_3;
wire alu_zero_3;
wire [1:0] Branch_3, MemtoReg_3;
wire RegWrite_3, MemRead_3, MemWrite_3;
wire [4:0] write_address_3;

// WB stage
wire [31:0] write_data;

//pipe
wire [31:0] mem_data_4, alu_result_4;
wire [4:0] write_address_4;
wire [1:0] MemtoReg_4;
wire RegWrite_4;

//--Components----------------------------------------------------------------------------------------------------
// Components in IF stage
MUX_2to1 #(.size(32)) pc_src_mux(
    .data0_i(pc_plus_4),
    .data1_i(branch_destination_3),
    .select_i(branch_select),
    .data_o(pc_next)
);

assign pc_plus_4 = pc_cur + 4;
ProgramCounter PC(
    .clk_i(clk_i),      
    .rst_i(rst_i),
    .pc_in_i(pc_next),
    .pc_out_o(pc_cur)
);

Instruction_Memory IM(
    .addr_i(pc_cur),
    .instr_o(instr)
);

Pipe_Reg #(.size(32)) IFID_PC_PLUS_4(
    .clk_i(clk_i),
    .rst_i(rst_i),
    .data_i(pc_plus_4),
    .data_o(pc_plus_4_1)
);

Pipe_Reg #(.size(32)) IFID_INSTR(
    .clk_i(clk_i),
    .rst_i(rst_i),
    .data_i(instr),
    .data_o(instr_1)
);

// Components in ID stage 
Reg_File RF(
    .clk_i(clk_i),
    .rst_i(rst_i),
    .RSaddr_i(instr_1[25:21]),
    .RTaddr_i(instr_1[20:16]),
    .RDaddr_i(write_address_4),
    .RDdata_i(write_data),
    .RegWrite_i(RegWrite_4),
    .RSdata_o(RSdata),  
    .RTdata_o(RTdata) 
);

Decoder decoder(
	.instr_op_i(instr_1[31:26]),
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

Sign_Extend sign_extend(
    .data_i(instr_1[15:0]),
    .data_o(immediate)
);

//pipe
Pipe_Reg #(.size(32)) IDEX_PC_PLUS_4(
    .clk_i(clk_i),
    .rst_i(rst_i),
    .data_i(pc_plus_4_1),
    .data_o(pc_plus_4_2)
);

Pipe_Reg #(.size(32)) IDEX_RSDATA(
    .clk_i(clk_i),
    .rst_i(rst_i),
    .data_i(RSdata),
    .data_o(RSdata_2)
);

Pipe_Reg #(.size(32)) IDEX_RTDATA(
    .clk_i(clk_i),
    .rst_i(rst_i),
    .data_i(RTdata),
    .data_o(RTdata_2)
);

Pipe_Reg #(.size(32)) IDEX_IMMEDIATE(
    .clk_i(clk_i),
    .rst_i(rst_i),
    .data_i(immediate),
    .data_o(immediate_2)
);

Pipe_Reg #(.size(5)) IDEX_RTADDR(
    .clk_i(clk_i),
    .rst_i(rst_i),
    .data_i(instr_1[20:16]),
    .data_o(write_addr_RT)
);

Pipe_Reg #(.size(5)) IDEX_RDADDR(
    .clk_i(clk_i),
    .rst_i(rst_i),
    .data_i(instr_1[15:11]),
    .data_o(write_addr_RD)
);

Pipe_Reg #(.size(2)) IDEX_ALUOP(
    .clk_i(clk_i),
    .rst_i(rst_i),
    .data_i(ALUOp),
    .data_o(ALUOp_2)
);

Pipe_Reg #(.size(1)) IDEX_ALUSRC(
    .clk_i(clk_i),   
    .rst_i(rst_i),
    .data_i(ALUSrc),
    .data_o(ALUSrc_2)
);

Pipe_Reg #(.size(1)) IDEX_REGWRITE(
    .clk_i(clk_i),
    .rst_i(rst_i),
    .data_i(RegWrite),
    .data_o(RegWrite_2)
);

Pipe_Reg #(.size(2)) IDEX_REGDST(
    .clk_i(clk_i),
    .rst_i(rst_i),
    .data_i(RegDst),
    .data_o(RegDst_2)
);

Pipe_Reg #(.size(2)) IDEX_BRANCH(
    .clk_i(clk_i),
    .rst_i(rst_i),
    .data_i(Branch),
    .data_o(Branch_2)
);

Pipe_Reg #(.size(1)) IDEX_MEMREAD(
    .clk_i(clk_i),
    .rst_i(rst_i),
    .data_i(MemRead),
    .data_o(MemRead_2)
);

Pipe_Reg #(.size(1)) IDEX_MEMWRITE(
    .clk_i(clk_i),
    .rst_i(rst_i),
    .data_i(MemWrite),
    .data_o(MemWrite_2)
);

Pipe_Reg #(.size(2)) IDEX_MEMTOREG(
    .clk_i(clk_i),
    .rst_i(rst_i),
    .data_i(MemtoReg),
    .data_o(MemtoReg_2)
);

// Components in EX stage	   
MUX_2to1 #(.size(32)) alu_src_mux(
    .data0_i(RTdata_2),
    .data1_i(immediate_2),
    .select_i(ALUSrc_2),
    .data_o(alu_src2)
);

ALU_Ctrl alu_ctrl(
    .funct_i(immediate_2[5:0]),
    .ALUOp_i(ALUOp_2),
    .ALUCtrl_o(ALUCtrl)
);

ALU alu(
    .src1_i(RSdata_2),
    .src2_i(alu_src2),
    .shamt_i(immediate_2[10:6]),
    .ctrl_i(ALUCtrl),
    .result_o(alu_result),
    .zero_o(alu_zero),
    .overflow(alu_overflow)
);

Shift_Left_Two_32 sl2(
    .data_i(immediate_2),
    .data_o(immsl2)
);

Adder adder(
    .src1_i(pc_plus_4_2),
	.src2_i(immsl2),
	.sum_o(branch_destination)
);

MUX_3to1 #(.size(5)) write_data_mux(
    .data0_i(write_addr_RT),
    .data1_i(write_addr_RD),
    .data2_i(5'b11111),
    .select_i(RegDst_2), // 2: $ra
    .data_o(write_address)
);

//pipe
Pipe_Reg #(.size(1)) EXMEM_REGWRITE(
    .clk_i(clk_i),
    .rst_i(rst_i),
    .data_i(RegWrite_2),
    .data_o(RegWrite_3)
);

Pipe_Reg #(.size(2)) EXMEM_MEMTOREG(
    .clk_i(clk_i),
    .rst_i(rst_i),
    .data_i(MemtoReg_2),
    .data_o(MemtoReg_3)
);

Pipe_Reg #(.size(2)) EXMEM_BRANCH(
    .clk_i(clk_i),
    .rst_i(rst_i),
    .data_i(Branch_2),
    .data_o(Branch_3)
);

Pipe_Reg #(.size(1)) EXMEM_MEMREAD(
    .clk_i(clk_i),
    .rst_i(rst_i),
    .data_i(MemRead_2),
    .data_o(MemRead_3)
);

Pipe_Reg #(.size(1)) EXMEM_MEMWRITE(
    .clk_i(clk_i),
    .rst_i(rst_i),
    .data_i(MemWrite_2),
    .data_o(MemWrite_3)
);

Pipe_Reg #(.size(32)) EXMEM_BRANCH_DESTINATION(
    .clk_i(clk_i),
    .rst_i(rst_i),
    .data_i(branch_destination),
    .data_o(branch_destination_3)
);

Pipe_Reg #(.size(1)) EXMEM_ALU_ZERO(
    .clk_i(clk_i),
    .rst_i(rst_i),
    .data_i(alu_zero),
    .data_o(alu_zero_3)
);

Pipe_Reg #(.size(32)) EXMEM_ALU_RESULT(
    .clk_i(clk_i),
    .rst_i(rst_i),
    .data_i(alu_result),
    .data_o(alu_result_3)
);

Pipe_Reg #(.size(32)) EXMEM_RTDATA(
    .clk_i(clk_i),
    .rst_i(rst_i),
    .data_i(RTdata_2),
    .data_o(RTdata_3)
);

Pipe_Reg #(.size(5)) EXMEM_WRITE_ADDR(
    .clk_i(clk_i),
    .rst_i(rst_i),
    .data_i(write_address),
    .data_o(write_address_3)
);

// Components in MEM stage
Data_Memory DM(
	.clk_i(clk_i),
	.addr_i(alu_result_3),
	.data_i(RTdata_3),
	.MemRead_i(MemRead_3), 
	.MemWrite_i(MemWrite_3),
	.data_o(mem_data)
);

assign branch_select = ((Branch_3 == 2'b01 && alu_zero_3) || (Branch_3 == 2'b10 && ~alu_zero_3))? 1 : 0;

//pipe
Pipe_Reg #(.size(1)) MEMWB_REGWRITE(
    .clk_i(clk_i),
    .rst_i(rst_i),
    .data_i(RegWrite_3),
    .data_o(RegWrite_4)
);

Pipe_Reg #(.size(2)) MEMWB_MEMTOREG(
    .clk_i(clk_i),
    .rst_i(rst_i),
    .data_i(MemtoReg_3),
    .data_o(MemtoReg_4)
);

Pipe_Reg #(.size(32)) MEMWB_MEM_DATA(
    .clk_i(clk_i),
    .rst_i(rst_i),
    .data_i(mem_data),
    .data_o(mem_data_4)
);

Pipe_Reg #(.size(32)) MEMWB_ALU_RESULT(
    .clk_i(clk_i),
    .rst_i(rst_i),
    .data_i(alu_result_3),
    .data_o(alu_result_4)
);

Pipe_Reg #(.size(5)) MEMWB_WRITE_ADDR(
    .clk_i(clk_i),
    .rst_i(rst_i),
    .data_i(write_address_3),
    .data_o(write_address_4)
);

// Components in WB stage
MUX_3to1 #(.size(32)) memtoreg_mux(
    .data0_i(alu_result_4),
    .data1_i(mem_data_4),
    .data2_i(0), //不會用到jal
    .select_i(MemtoReg_4), // 2: PC+4 for $ra
    .data_o(write_data)
);

endmodule