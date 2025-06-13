// 112550020
module Adder(
    src1_i,
	src2_i,
	sum_o
	);

// TO DO
     
// I/O ports
input  [32-1:0]  src1_i;
input  [32-1:0]	 src2_i;

output [32-1:0]	 sum_o;

// Internal Signals


// Main function
assign sum_o = src1_i + src2_i;


endmodule                  