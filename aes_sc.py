import os 
import siliconcompiler

def aes_asic(design="aes_128"):
    chip = siliconcompiler.Chip(design)
    chip.input("./rtl/round.v")
    chip.input("./rtl/table.v")
    chip.input(f"./rtl/{design}.v")
    chip.input("./constraints/constraints_128.sdc")
    chip.load_target("skywater130_demo")
    chip.run()
    chip.summary()

if __name__ == "__main__":
    aes_asic(design="aes_128")