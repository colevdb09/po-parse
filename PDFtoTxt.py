import os

# Create text file from pdf
for filename in os.listdir(os.getcwd()):
    if filename.endswith(".pdf"):
        os.system('pdftotext -layout ' + filename)

# Create a list of each line in the text file
for filename in os.listdir(os.getcwd()):
    if filename.endswith(".txt"):
        f = open(filename, 'r')
        f_list = []
        lineIndex = 0

        for x in f:
            f_list.append(x)

        # Create a list of each lines quantity, product, and unit price
        po = f_list[0].split()[2]
        LineItems = []

        # Determine number of lines in the PO
        if f_list[37].split()[0] == '2':
            txtLine = [26,37]
        else:
            txtLine = [26]

        for n in txtLine:

            # Creates a dictionary for each line item
            def parser(p):
                line = {}
                line['quantity'] = f_list[n].split()[1]
                line['product'] = f_list[n + 1].split()[0][0:7] + p + f_list[n + 1].split()[0][10:]
                line['unit'] = float(f_list[n].split()[3])
                LineItems.append(line)

            # Calculates the price for each product in a bundle
            def priceCalc(prod, fleetMult, adtchMult,index):
                target = round(float(f_list[n].split()[3]), 2)
                total = 0
                for i in LineItems[index:]:
                    if i['product'].find('FLT') != -1:
                        i['unit'] = round(i['unit'] * fleetMult, 2)
                    else:
                        i['unit'] = round(i['unit'] * adtchMult, 2)
                    total += i['unit']
                dif =  target - total
                if dif != 0:
                    LineItems[index + len(prod) - 1]['unit'] = round(LineItems[index + len(prod) - 1]['unit'] + dif, 2)

            # Determine if the product is a bundle
            product = f_list[n + 1].split()[0][7:10]

            # Admin Teacher Bundle
            # STILL NEED TO ACCOUNT FOR MULTIPLE BUNDLES IE THE PRICECALC FUNCTION
            if product == "BAT":
                products = ['ADM', 'TCR']
                map(parser, products)

                # Check for the odd penny
                if int(LineItems[lineIndex]['unit'] * 100) % 2 != 0:
                    LineItems[lineIndex]['unit'] = LineItems[lineIndex]['unit'] / 2 + 0.005
                    LineItems[lineIndex+1]['unit'] = LineItems[lineIndex+1]['unit'] / 2 - 0.005
                else:
                    for i in LineItems[lineIndex:]:
                        i['unit'] = i['unit']/2
                lineIndex += len(products)

            # Admin / Teacher / Fleet Bundle
            elif product == "ATF":
                products = ['ADM', 'TCR', 'FLT']
                map(parser, products)
                priceCalc(products, 0.1666, 0.4167, lineIndex)
                lineIndex += len(products)

            # Teacher / Fleet Bundle
            elif product == "BTF":
                products = ['TCR', 'FLT']
                map(parser, products)
                priceCalc(products, 0.2857, 0.7142, lineIndex)
                lineIndex += len(products)

            # Admin / Fleet / Bundle
            elif product == "BAF":
                products = ['ADM', 'FLT']
                map(parser, products)
                priceCalc(products, 0.2857, 0.7142, lineIndex)
                lineIndex += len(products)

            # single product line item
            else:
                # Create dictionary for the line item
                line = {}
                line['quantity'] = f_list[n].split()[1]
                line['product'] = f_list[n+1].split()[0]
                line['unit'] = f_list[n].split()[3]
                LineItems.append(line)
                lineIndex += 1

        # Print lines under each PO
        print '-------------------------------', '\n', 'PO #', po
        for n in LineItems:
            print 'Quantity: ', n['quantity']
            print 'Product: ', n['product']
            print 'Unit Price: $', n['unit']
            print '\n'

        f.close()
