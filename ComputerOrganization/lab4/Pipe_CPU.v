// ID

`include "Adder.v"
`include "ALU_Ctrl.v"
`include "ALU.v"
`include "Reg_File.v"
`include "Data_Memory.v"
`include "Decoder.v"
`include "Instruction_Memory.v"
// `include "MUX_2to1.v"
`include "Pipe_Reg.v"
`include "ProgramCounter.v"
`include "Shift_Left_Two_32.v"
`include "Sign_Extend.v"

`timescale 1ns / 1ps

module Pipe_CPU(
    clk_i,
    rst_i
    );

input clk_i;
input rst_i;

// TO DO

// Internal signal

// IF stage


// ID stage


// EX stage


// MEM stage


// WB stage


// Components

// Components in IF stage



// Components in ID stage



// Components in EX stage	   



// Components in MEM stage



// Components in WB stage


endmodule