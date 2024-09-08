osSubroutines = {
            # Output class
            "Output.init":{"returnType":"void","kind":"function"},
            "Output.moveCursor":{"returnType":"void","kind":"function"},
            "Output.printChar": {"returnType":"void","kind":"function"},
            "Output.printString": {"returnType":"void","kind":"function"},
            "Output.printInt": {"returnType":"void","kind":"function"},
            "Output.println": {"returnType":"void","kind":"function"},
            "Output.backSpace": {"returnType":"void","kind":"function"},

            # Screen class
            "Screen.init":{"returnType":"void","kind":"function"},
            "Screen.clearScreen": {"returnType":"void","kind":"function"},
            "Screen.setColor": {"returnType":"void","kind":"function"},
            "Screen.drawPixel": {"returnType":"void","kind":"function"},
            "Screen.drawLine": {"returnType":"void","kind":"function"},
            "Screen.drawRectangle": {"returnType":"void","kind":"function"},
            "Screen.drawCircle": {"returnType":"void","kind":"function"},

            # Keyboard class
            "Keyboard.init":{"returnType":"void","kind":"function"},
            "Keyboard.keyPressed": {"returnType":"char","kind":"function"},
            "Keyboard.readChar": {"returnType":"char","kind":"function"},
            "Keyboard.readLine": {"returnType":"String","kind":"function"},
            "Keyboard.readInt": {"returnType":"int","kind":"function"},
            

            # Memory class
            "Memory.init":{"returnType":"void","kind":"function"},
            "Memory.peek": {"returnType":"int","kind":"function"},
            "Memory.poke": {"returnType":"void","kind":"function"},
            "Memory.alloc": {"returnType":"Array","kind":"function"},
            "Memory.deAlloc": {"returnType":"void","kind":"function"},

            # Math class
            "Math.init":{"returnType":"void","kind":"function"},
            "Math.abs": {"returnType":"int","kind":"function"},
            "Math.multiply": {"returnType":"int","kind":"function"},
            "Math.divide": {"returnType":"int","kind":"function"},
            "Math.min": {"returnType":"int","kind":"function"},
            "Math.max": {"returnType":"int","kind":"function"}, 
            "Math.sqrt": {"returnType":"int","kind":"function"},

            # String class
            "String.new": {"returnType":"String","kind":"constructor"},
            "String.dispose": {"returnType":"void","kind":"method"},
            "String.length": {"returnType":"int","kind":"method"},
            "String.charAt": {"returnType":"char","kind":"method"},
            "String.setCharAt": {"returnType":"void","kind":"method"},
            "String.appendChar": {"returnType":"String","kind":"method"},
            "String.eraseLastChar": {"returnType":"void","kind":"method"},
            "String.intValue": {"returnType":"int","kind":"method"},
            "String.setInt": {"returnType":"void","kind":"method"},
            "String.backSpace": {"returnType":"char","kind":"function"},
            "String.doubleQuote": {"returnType":"char","kind":"function"},
            "String.newLine": {"returnType":"char","kind":"function"},

            # Array class
            "Array.new": {"returnType":"Array","kind":"function"},
            "Array.dispose": {"returnType":"void","kind":"method"},

            # Sys class
            "Sys.init":{"returnType":"void","kind":"function"},
            "Sys.halt": {"returnType":"void","kind":"function"},
            "Sys.error": {"returnType":"void","kind":"function"},
            "Sys.wait": {"returnType":"void","kind":"function"}
        }
