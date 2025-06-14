// 112550020
module MUX_2to1(
               data0_i,
               data1_i,
               select_i,
               data_o
               );

// TO DO

parameter size = 32;
			
// I/O ports               
input       [size-1:0] data0_i;
input       [size-1:0] data1_i;
input                  select_i;

output  reg [size-1:0] data_o; 

// Internal Signals


// Main function
always@(*)begin
    data_o = select_i? data1_i: data0_i;
end

endmodule      
