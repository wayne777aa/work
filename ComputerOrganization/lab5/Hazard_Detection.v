// 112550020
module Hazard_Detection(
    idex_memread,
    instr_i,    // IF/ID 的 instruction
    idex_regt,  // lw 的 rt
    branch,     // mem 的 branch_select
    pcwrite,
    ifid_write,
    ifid_flush,
    idex_flush,
    exmem_flush
);

// TO DO
input        idex_memread;
input [31:0] instr_i;
input [ 4:0] idex_regt;
input        branch;

output reg pcwrite, ifid_write;
output reg ifid_flush, idex_flush, exmem_flush;

// 拆出 IF/ID 階段的 rs, rt
wire [4:0] ifid_rs = instr_i[25:21];
wire [4:0] ifid_rt = instr_i[20:16];

always @(*) begin
    pcwrite     = 1'b1;
    ifid_write  = 1'b1;
    ifid_flush  = 1'b0;
    idex_flush  = 1'b0;
    exmem_flush = 1'b0;

    // branch hazard
    if (branch) begin
        // EX 階段 branch 決定後，要把 IF/ID、ID/EX (和 EX/MEM) 裡的「錯抓」指令全 flush
        ifid_flush  = 1'b1;
        idex_flush  = 1'b1;
        exmem_flush = 1'b1;
        // PC 直接依 branch target 更新，IF/ID 換成正確的 next-PC instr
    end
    // load-use hazard
    else if(idex_memread
            && ((idex_regt == ifid_rs) || (idex_regt == ifid_rt))) begin
        // PC, IF/ID 不更新; ID/EX bubble
        pcwrite    = 1'b0;
        ifid_write = 1'b0;
        idex_flush = 1'b1;
    end
    
end

endmodule