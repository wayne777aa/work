// 112550020
module Forwarding_Unit(
    regwrite_exmem, // EX_MEM_RegWrite
    regwrite_memwb, // regwrite_wb
    idex_regs,      // ID_EX_Register的Rs
    idex_regt,      // ID_EX_Register的Rt
    exmem_regd,
    memwb_regd,
    forwarda,
    forwardb
);

// TO DO
// I/O ports
input       regwrite_exmem, regwrite_memwb;
input [4:0] idex_regs, idex_regt;
input [4:0] exmem_regd, memwb_regd;
output reg [1:0] forwarda, forwardb;

always @(*) begin
    // 預設：不轉發
    forwarda = 2'b00;
    forwardb = 2'b00;

    // 判斷 A 端 (rs)
    if (regwrite_exmem && (exmem_regd != 0) 
        && (exmem_regd == idex_regs))
        forwarda = 2'b10;  // 從 EX/MEM 轉發
    else if (regwrite_memwb && (memwb_regd != 0) 
        && (memwb_regd == idex_regs))
        forwarda = 2'b01;  // 從 MEM/WB 轉發

    // 判斷 B 端 (rt)
    if (regwrite_exmem && (exmem_regd != 0)
        && (exmem_regd == idex_regt))
        forwardb = 2'b10;
    else if (regwrite_memwb && (memwb_regd != 0)
        && (memwb_regd == idex_regt))
        forwardb = 2'b01;
end


endmodule