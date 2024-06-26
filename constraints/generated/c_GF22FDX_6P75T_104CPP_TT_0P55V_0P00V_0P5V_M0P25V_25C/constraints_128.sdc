
# 200MHz
set clock_period 0.33


# OBI inputs delays
set in_delay    [expr $clock_period * 0.80]

# OBI outputs delays
set out_delay [expr $clock_period * 0.60]

# All clocks
set clock_ports [list \
    clk \
]

# IRQ Input ports
set input_ports [list \
    state \
    key \
    ]

# IRQ Output ports
set output_ports [list \
    out \
]



############## Defining default clock definitions ##############

#create_clock -period 40 -waveform {0 20} -name clk
create_clock \
      -name clk \
      -period $clock_period \
      [get_ports clk] 


########### Defining Default I/O constraints ###################

set all_clock_ports $clock_ports

# IRQs
set_input_delay  $in_delay       [get_ports $input_ports        ] -clock clk
set_output_delay $out_delay      [get_ports $output_ports       ] -clock clk