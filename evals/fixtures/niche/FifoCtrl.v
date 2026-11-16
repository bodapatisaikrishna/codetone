`define width 8

module fifo_ctrl (clk, reset_l, push, pop, full, empty);
    parameter depth = 4;
    input clk, reset_l, push, pop;
    output full, empty;
    reg [`width-1:0] count;
    reg full, empty;

    typedef enum logic [1:0] {IDLE, BUSY, DONE} state_t;
    state_t state;

    always @(posedge clk or negedge reset_l)
        if (!reset_l) count = 0;
        else if (push) count = count + 1;
        else if (pop) count = count - 1;

    always @(count or depth) begin
        full <= (count == depth);
        empty <= (count == 0);
        #1 busy_flag = full & empty;
    end

    genvar i;
    generate
        for (i = 0; i < depth; i = i + 1) begin
            dff u_dff (clk, push, q[i]);
        end
    endgenerate

    always @(*) begin
        case (state)
            IDLE: state = BUSY;
            BUSY: state = DONE;
        endcase
    end
endmodule
