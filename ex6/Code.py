class Code:
    def __init__(self):
        self.destCodes = {'null': '000', 'M': '001', 'D': '010', 'MD': '011',
                          'A': '100', 'AM': '101', 'AD': '110', 'AMD': '111'}

        self.compCodes = {'0': '110101010', '1': '110111111',
                          '-1': '110111010', 'D': '110001100',
                          'A': '110110000', 'M': '111110000',
                          '!D': '110001101', '!A': '110110001',
                          '!M': '111110001', '-D': '110001111',
                          '-A': '110110011', '-M': '111110011',
                          'D+1': '110011111', 'A+1': '110110111',
                          'M+1': '111110111', 'D-1': '110001110',
                          'A-1': '110110010', 'M-1': '111110010',
                          'D+A': '110000010', 'D+M': '111000010',
                          'D-A': '110010011', 'D-M': '111010011',
                          'A-D': '110000111', 'M-D': '111000111',
                          'D&A': '110000000', 'D&M': '111000000',
                          'D|A': '110010101', 'D|M': '111010101'}

        self.jumpCodes = {'null': '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011',
                          'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111'}

    def dest(self, mnemonic):
        return self.destCodes[mnemonic]

    def comp(self, mnemonic):
        return self.compCodes[mnemonic]

    def jump(self, mnemonic):
        return self.jumpCodes[mnemonic]