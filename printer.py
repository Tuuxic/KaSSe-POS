from escpos.printer import Serial

PRINTER_PATH = '/dev/ttyS4'

p = Serial(PRINTER_PATH, baudrate=115200)

p.set(align='center')

p.barcode(code='{3118512', bc='CODE128', check=False)

p.cut()
