// 112550020
module ALU_Ctrl(
    funct_i,
    ALUOp_i,
    ALUCtrl_o
);
          
// TO DO
// I/O ports 
input      [6-1:0] funct_i;
input      [2-1:0] ALUOp_i;

output reg [4-1:0] ALUCtrl_o;  
     
// Internal Signals


// Main function
always @(*) begin
    case (ALUOp_i)
        2'b00: ALUCtrl_o = 4'b0010; // addi, lw, sw
        2'b01: ALUCtrl_o = 4'b0110; // beq, bne
        2'b10: begin              // R-type
            case (funct_i)
                6'b100010: ALUCtrl_o = 4'b0010; // add
                6'b100000: ALUCtrl_o = 4'b0110; // sub
                6'b100101: ALUCtrl_o = 4'b0000; // and
                6'b100100: ALUCtrl_o = 4'b0001; // or
                6'b101010: ALUCtrl_o = 4'b1100; // nor
                6'b100111: ALUCtrl_o = 4'b0111; // slt
                6'b000000: ALUCtrl_o = 4'b1000; // sll
                6'b000010: ALUCtrl_o = 4'b1001; // srl
                6'b000100: ALUCtrl_o = 4'b1010; // sllv
                6'b000110: ALUCtrl_o = 4'b1011; // srlv
                6'b001000: ALUCtrl_o = 4'b1111; // jr
                default:   ALUCtrl_o = 4'b0000; // default = and
            endcase
        end
        default: ALUCtrl_o = 4'b0000; // default = and
    endcase
end  

endmodule
