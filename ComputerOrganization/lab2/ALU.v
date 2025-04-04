`timescale 1ns/1ps
`include "ALU_1bit.v"
module ALU(
	input                   rst_n,         // negative reset            (input)
	input	     [32-1:0]	src1,          // 32 bits source 1          (input)
	input	     [32-1:0]	src2,          // 32 bits source 2          (input)
	input 	     [ 4-1:0] 	ALU_control,   // 4 bits ALU control input  (input)
	output reg   [32-1:0]	result,        // 32 bits result            (output)
	output reg              zero,          // 1 bit when the output is 0, zero must be set (output)
	output reg              cout,          // 1 bit carry out           (output)
	output reg              overflow       // 1 bit overflow            (output)
	);

wire [32:0]	cin;
assign cin[0] = (ALU_control == 4'b0110 || ALU_control == 4'b0111) ? 1'b1 : 1'b0; //如果是減法需要+1
wire [31:0] rawresult;

ALU_1bit A0(
	.src1(src1[0]),       
	.src2(src2[0]),       
	.less(1'b0),       
	.Ainvert(ALU_control[3]),    
	.Binvert(ALU_control[2]),    
	.cin(cin[0]),
	.operation(ALU_control[1:0]),  
	.result(rawresult[0]),
	.cout(cin[1])
);

genvar i;
generate
    for (i = 1; i < 31; i = i + 1) begin
        ALU_1bit A1to30(
            .src1(src1[i]),
            .src2(src2[i]),
            .less(1'b0),
            .Ainvert(ALU_control[3]),
            .Binvert(ALU_control[2]),
            .cin(cin[i]),
            .operation(ALU_control[1:0]),
            .result(rawresult[i]),
            .cout(cin[i+1])
        );
    end
endgenerate

ALU_1bit A31(
	.src1(src1[31]),       
	.src2(src2[31]),       
	.less(1'b0),       
	.Ainvert(ALU_control[3]),    
	.Binvert(ALU_control[2]),    
	.cin(cin[31]),
	.operation(ALU_control[1:0]),  
	.result(rawresult[31]),
	.cout(cin[32])
);

reg set;

always @(*) begin
	set = cin[31] ^ cin[32] ^ rawresult[31];
    case (ALU_control)
        4'b0111: begin
			result[0] = set;  // SLT only affects bit 0
			result[31:1] = 0;
			overflow = 0; //因為overflow可能會是1 但是SLT的V是0
			cout = 0; //cin[32]可能是1,因為要檢查overflow, 但是SLT的C是0
		end
		default: begin //正常運作
			result = rawresult;
			overflow = cin[31] ^ cin[32];
			cout = cin[32];
		end
    endcase
	zero = (result == 0);
end

endmodule

