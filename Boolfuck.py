class Boolfuck_Interpreter():
    def __init__(self):
        self.tape = [0] * 30000
        pass
    
    def __get_matching_bracket(self, index, code):
        counter = 0  
        if code[index] == "[":
            for i in range(index, len(code)):
                if code[i] == "[": counter += 1
                elif code[i] == "]": counter -= 1

                if counter == 0: 
                    return(i)
        else:
            for i in range(index, 0, -1):
                if code[i] == "[": counter -= 1
                elif code[i] == "]": counter += 1

                if counter == 0: 
                    return(i)

    #Convert a character from the input stream to bits
    def __input_to_bits(self, input):
        input_bits = []
        for x in input:
            input_bits.append(format(ord(x), 'b'))
            
        for i, x in enumerate(input_bits):
            while(len(input_bits[i]) < 8): input_bits[i] = "0" + input_bits[i]
                
            #It is already in the right order and on its own does not need to be reversed
            #However, if left as is, it will be reversed into the wrong order at the end of the interpretation
            input_bits[i] = input_bits[i][::-1] 
        return ''.join(input_bits)

    #Interpret and execute the boolfuck code
    def execute_boolfuck(self, code, input="", printout=True, cleartape=True):
        if cleartape:
            self.tape = [0] * 30000
        pointer = code_index = input_index = 0
        input_converted = self.__input_to_bits(input)
        
        #Parsing time
        output = ""
        while code_index < len(code):
            instruction = code[code_index]
            if instruction == '+': self.tape[pointer] = int(not self.tape[pointer])
            if instruction == '<': pointer += 1
            if instruction == '>': pointer -= 1
            if instruction == '[' and self.tape[pointer] == 0: 
                code_index = self.__get_matching_bracket(code_index, code)
            if instruction == ']' and self.tape[pointer] == 1:
                code_index = self.__get_matching_bracket(code_index, code) 
            if instruction == ';': 
                output += str(self.tape[pointer])
            if instruction == ',' and input_index < len(input_converted): 
                    self.tape[pointer] = int(input_converted[input_index])
                    input_index += 1
            code_index += 1
        
        #End-of-file, set bit under pointer to zero
        self.tape[pointer] = 0
        
        #Padding the output until it's divisible by eight
        while(len(output) > 0 and len(output) % 8 != 0):
            output += "0"
        
        #Fixing up the output
        buffer = ""
        output_formatted = ""
        for x in output:
            buffer += x
                    
            if len(buffer) == 8:
                #Reverse into the correct order, convert to char, add to formatted output, clear buffer
                buffer = buffer[::-1]
                converted_char = chr(int(buffer, 2))
                output_formatted += converted_char
                buffer = ""
        
        if printout:
            print(output_formatted)        
        return(output_formatted)

    def execute_brainfuck(self, brainfuck_code, input="", printout=True, cleartape=True):
        return(self.execute_boolfuck(self.brainfuck_to_boolfuck(brainfuck_code), input, printout, cleartape))
    
    def brainfuck_to_boolfuck(self, brainfuck_code):
        boolfuck_code = ""
        replacements = {
            "+": ">[>]+<[+<]>>>>>>>>>[+]<<<<<<<<<",
            "-": ">>>>>>>>>+<<<<<<<<+[>+]<[<]>>>>>>>>>[+]<<<<<<<<<",
            "<": "<<<<<<<<<",
            ">": ">>>>>>>>>",
            ",": ">,>,>,>,>,>,>,>,<<<<<<<<",
            ".": ">;>;>;>;>;>;>;>;<<<<<<<<",
            "[": ">>>>>>>>>+<<<<<<<<+[>+]<[<]>>>>>>>>>[+<<<<<<<<[>]+<[+<]",
            "]": ">>>>>>>>>+<<<<<<<<+[>+]<[<]>>>>>>>>>]<[+<]"
        }
        
        for x in brainfuck_code:
            boolfuck_code += replacements[x]
        
        return boolfuck_code
