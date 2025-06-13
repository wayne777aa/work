// 112550020
module Shift_Left_Two_32(
    data_i,
    data_o
    );

// TO DO
// I/O ports                    
input   [32-1:0] data_i;

output  [32-1:0] data_o;

// Internal Signals


// Main function
assign data_o =  data_i << 2;
     
endmodule
