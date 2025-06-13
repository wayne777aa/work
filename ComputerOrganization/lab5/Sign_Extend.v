// 112550020
module Sign_Extend(
    data_i,
    data_o
    );
               
// TO DO
// I/O ports
input   [16-1:0] data_i;

output  [32-1:0] data_o;

// Internal Signals


// Main function
assign data_o = {{16{data_i[15]}}, data_i};
           
endmodule      
     