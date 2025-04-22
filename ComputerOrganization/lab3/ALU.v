// 112550020
`include "MUX_2to1.v"
//------------------------------------------------------------------------------------------------------

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

MUX_2to1 #(.size(1)) aselect(
    .data0_i(src1),
    .data1_i(~src1),
    .select_i(Ainvert),
    .data_o(a)
);


MUX_2to1 #(.size(1)) bselect(
    .data0_i(src2),
    .data1_i(~src2),
    .select_i(Binvert),
    .data_o(b)
);
wire opand, opor, opadd;
assign opand = a&b;
assign opor = a|b;
assign sum = a^b^cin;

always @(*) begin
	case (operation)
		2'b00: begin // and
			result = opand;
			cout = 0;
		end
		2'b01: begin // or
			result = opor;
			cout = 0;
		end
		2'b10: begin // sum
			result = sum;
			cout = (a & b) | (a & cin) | (b & cin);
		end
		2'b11: begin // slt
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
//------------------------------------------------------------------------------------------------------
module ALU(
	input	     [32-1:0]	src1_i,         // 32 bits source 1          (input)
	input	     [32-1:0]	src2_i,         // 32 bits source 2          (input)
	input      	 [ 5-1:0] 	shamt_i,
	input 	     [ 4-1:0] 	ctrl_i,   		// 4 bits ALU control input  (input)
	output reg   [32-1:0]	result_o,       // 32 bits result            (output)
	output reg              zero_o,         // 1 bit when the output is 0, zero must be set (output)
	output reg              overflow       	// 1 bit overflow            (output)
	);

wire [32:0]	cin;
assign cin[0] = (ctrl_i == 4'b0110 || ctrl_i == 4'b0111) ? 1'b1 : 1'b0; // 如果是減法需要+1
wire [31:0] rawresult;
reg set;

ALU_1bit A0(
	.src1(src1_i[0]),       
	.src2(src2_i[0]),       
	.less(1'b0),       
	.Ainvert(ctrl_i[3]),    
	.Binvert(ctrl_i[2]),    
	.cin(cin[0]),
	.operation(ctrl_i[1:0]),  
	.result(rawresult[0]),
	.cout(cin[1])
);

genvar i;
generate
    for (i = 1; i < 31; i = i + 1) begin
        ALU_1bit A1to30(
            .src1(src1_i[i]),
            .src2(src2_i[i]),
            .less(1'b0),
            .Ainvert(ctrl_i[3]),
            .Binvert(ctrl_i[2]),
            .cin(cin[i]),
            .operation(ctrl_i[1:0]),
            .result(rawresult[i]),
            .cout(cin[i+1])
        );
    end
endgenerate

ALU_1bit A31(
	.src1(src1_i[31]),       
	.src2(src2_i[31]),       
	.less(1'b0),       
	.Ainvert(ctrl_i[3]),    
	.Binvert(ctrl_i[2]),    
	.cin(cin[31]),
	.operation(ctrl_i[1:0]),  
	.result(rawresult[31]),
	.cout(cin[32])
);

always @(*) begin
	set = cin[31] ^ cin[32] ^ rawresult[31]; // overflow ^ result[31](111負數 set=1)(101正overflow set=0)(010負overflow set=1)
	case (ctrl_i)
		4'b0111: begin //slt
			result_o[0] = set;  // SLT only affects bit 0
			result_o[31:1] = 0;
			overflow = 0; // 因為overflow可能會是1 但是SLT的V是0
		end
		4'b1000: begin // sll (shamt)
			result_o = src2_i << shamt_i; // src1_i = shamt
			overflow = 0;
		end
		4'b1001: begin // srl (shamt)
			result_o = src2_i >> shamt_i; // src1_i = shamt
			overflow = 0;
		end
		4'b1010: begin // sllv (rs)
			result_o = src2_i << src1_i[4:0]; // src1_i = rs
			overflow = 0;
		end
		4'b1011: begin // srlv (rs)
			result_o = src2_i >> src1_i[4:0]; // src1_i = rs
			overflow = 0;
		end
		default: begin // 正常運作
			result_o = rawresult;
			overflow = cin[31] ^ cin[32];
		end
	endcase
	zero_o = (result_o == 0);
end

endmodule