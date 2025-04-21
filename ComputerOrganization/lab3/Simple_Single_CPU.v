// 112550020

`include "ProgramCounter.v"
`include "Instr_Memory.v"
`include "Reg_File.v"
`include "Data_Memory.v"


module Simple_Single_CPU(
        clk_i,
	rst_i
);
		
// I/O port
input         clk_i;
input         rst_i;

// Internal Signals


// Components
ProgramCounter PC(
        .clk_i(),      
        .rst_i(),     
        .pc_in_i(),   
        .pc_out_o() 
);

Instr_Memory IM(
        .pc_addr_i(),  
        .instr_o()    
);

Reg_File Registers(
        .clk_i(),
        .rst_i() ,     
        .RSaddr_i(),
        .RTaddr_i(),
        .RDaddr_i(), 
        .RDdata_i(),
        .RegWrite_i(),
        .RSdata_o(),  
        .RTdata_o() 
);
	
Data_Memory Data_Memory(
	.clk_i(), 
	.addr_i(), 
	.data_i(), 
	.MemRead_i(), 
	.MemWrite_i(), 
	.data_o()
);

endmodule
