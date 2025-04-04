`timescale 1ns/1ps

module MUX_2to1(
	input      src1,
	input      src2,
	input	   select,
	output reg result
	);

always @(*) begin
	result = select? src2: src1;
end


endmodule

