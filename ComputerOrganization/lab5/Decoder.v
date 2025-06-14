// 112550020
module Decoder( 
	instr_op_i, 
	ALUOp_o, 
	ALUSrc_o,
	RegWrite_o,	
	RegDst_o,
	Branch_o,
	Jump_o, // not needed
	MemRead_o, 
	MemWrite_o, 
	MemtoReg_o,
);
     
// TO DO
// I/O ports
input		[6-1:0] instr_op_i;

output	reg [2-1:0] ALUOp_o; // 00加法;01減法;10 R-type;
output	reg	[2-1:0] RegDst_o, MemtoReg_o; // regdst 使用2 選 $ra (reg 31) // MemtoReg 使用2 寫入 PC+4
output  reg	[2-1:0] Branch_o; // 使用 2 表示 bne 分支，需 MUX_3to1 處理
output	reg			ALUSrc_o, RegWrite_o, Jump_o, MemRead_o, MemWrite_o;

// Internal Signals


// Main function
always@(*)begin
	case (instr_op_i)
		6'b000000: 	begin	// R-type
			RegDst_o 	= 1;
			Jump_o 		= 0;
			Branch_o 	= 0;
			MemRead_o 	= 0;
			MemtoReg_o 	= 0;
			ALUOp_o 	= 2'b10;
			MemWrite_o 	= 0;
			ALUSrc_o 	= 0;
			RegWrite_o 	= 1;
		end
		6'b001000: 	begin	// addi
			RegDst_o 	= 0;
			Jump_o 		= 0;
			Branch_o 	= 0;
			MemRead_o 	= 0;
			MemtoReg_o 	= 0;
			ALUOp_o 	= 2'b00;
			MemWrite_o 	= 0;
			ALUSrc_o 	= 1;
			RegWrite_o 	= 1;
		end
		6'b101011: 	begin	// lw
			RegDst_o 	= 0;
			Jump_o 		= 0;
			Branch_o 	= 0;
			MemRead_o 	= 1;
			MemtoReg_o 	= 1;
			ALUOp_o 	= 2'b00;
			MemWrite_o 	= 0;
			ALUSrc_o 	= 1;
			RegWrite_o 	= 1;
		end
		6'b100011: 	begin	// sw
			RegDst_o 	= 0;
			Jump_o 		= 0;
			Branch_o 	= 0;
			MemRead_o 	= 0;
			MemtoReg_o 	= 0;
			ALUOp_o 	= 2'b00;
			MemWrite_o 	= 1;
			ALUSrc_o 	= 1;
			RegWrite_o 	= 0;
		end
		6'b000101: 	begin	// beq
			RegDst_o 	= 0;
			Jump_o 		= 0;
			Branch_o 	= 1;
			MemRead_o 	= 0;
			MemtoReg_o 	= 0;
			ALUOp_o 	= 2'b01;
			MemWrite_o 	= 0;
			ALUSrc_o 	= 0;
			RegWrite_o 	= 0;
		end
		6'b000100: 	begin	// bne
			RegDst_o 	= 0;
			Jump_o 		= 0;
			Branch_o 	= 2; // 使用 2 表示 bne 分支，需 MUX_3to1 處理
			MemRead_o 	= 0;
			MemtoReg_o 	= 0;
			ALUOp_o 	= 2'b01;
			MemWrite_o 	= 0;
			ALUSrc_o 	= 0;
			RegWrite_o 	= 0;
		end
		6'b000011: 	begin	// j
			RegDst_o 	= 0;
			Jump_o 		= 1;
			Branch_o 	= 0;
			MemRead_o 	= 0;
			MemtoReg_o 	= 0;
			ALUOp_o 	= 2'b00;
			MemWrite_o 	= 0;
			ALUSrc_o 	= 0;
			RegWrite_o 	= 0;
		end
		6'b000010: 	begin	// jal
			RegDst_o 	= 2; // 選 $ra (reg 31)
			Jump_o 		= 1;
			Branch_o 	= 0;
			MemRead_o 	= 0;
			MemtoReg_o 	= 2; // 寫入 PC+4
			ALUOp_o 	= 2'b00;
			MemWrite_o 	= 0;
			ALUSrc_o 	= 0;
			RegWrite_o 	= 1;
		end
		default:	begin
			RegDst_o 	= 0;
			Jump_o 		= 0;
			Branch_o 	= 0;
			MemRead_o 	= 0;
			MemtoReg_o 	= 0;
			ALUOp_o 	= 2'b00;
			MemWrite_o 	= 0;
			ALUSrc_o 	= 0;
			RegWrite_o 	= 0;
		end
	endcase
end

endmodule