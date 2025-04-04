`timescale 1ns/1ps
`include "MUX_2to1.v"
`include "MUX_4to1.v"

module ALU_1bit(
	input				src1,       //1 bit source 1  (input)
	input				src2,       //1 bit source 2  (input)
	input				less,       //1 bit less      (input)
	input 				Ainvert,    //1 bit A_invert  (input)
	input				Binvert,    //1 bit B_invert  (input)
	input 				cin,        //1 bit carry in  (input)
	input 	    [2-1:0] operation,  //2 bit operation (input)
	output reg          result,     //1 bit result    (output)
	output reg          cout        //1 bit carry out (output)
	);
		
wire a,b,sum;

MUX_2to1 aselect(
	.src1(src1),
	.src2(~src1),
	.select(Ainvert),
	.result(a)
	);
MUX_2to1 bselect(
	.src1(src2),
	.src2(~src2),
	.select(Binvert),
	.result(b)
	);
// assign a = Ainvert? ~src1 : src1;
// assign b = Binvert? ~src2 : src2;
wire opand, opor, opadd;
assign opand = a&b;
assign opor = a|b;
assign sum = a^b^cin;

always @(*) begin
	case (operation)
		2'b00: begin
			result = opand;
			cout = 0;
		end
		2'b01: begin
			result = opor;
			cout = 0;
		end
		2'b10: begin
			result = sum;
			cout = (a & b) | (a & cin) | (b & cin);
		end
		2'b11: begin
			result = sum; //為了set
			cout = (a & b) | (a & cin) | (b & cin); //為了檢查overflow給set用
		end
		default: begin
			result = 0;
			cout = 0;
		end
	endcase
end
endmodule
