import constants as cs
import shlex
from unidecode import unidecode


class FileHandler:
    '''
    FileHandler: main class that encapsulates the functionality of the program.
    :param filename: Path to Customer input sample file
    :type coords: str
    '''

    def __init__(self, filename=None):
        if filename is None:
            raise ValueError("File name cannot be none.")

        self.input_file = open(filename, encoding='utf-8')

    @property
    def test_customers(self):
        """
        Class property. It reads all customers from sample input file and stores them in a list.
        Then returns the list.
        :rtype: list
        """
        customers = []

        for line in self.input_file:
            line = unidecode(line).replace('"', '').strip()
            customers.append(line)

        # remove header from list.
        customers.pop(0)
        return customers

    def join(self, filename, header=[], target=None):
        '''
        Takes as input a csv file and stores only the pre-selected customer data in a dictionary.
        The dict object has as keys the fields (str) of the csv and as values the extracted customer data in lists.
        Target is a list of that is used as reference to extract customer data. For example in "CUSTOMER.csv" target is
        the list with all the "CUSTOMER_CODES" we need. In "INVOICE_ITEM.csv", target is the list with all the "INVOICE_CODE"
        lines we need to extract.

        Example
        ---------
        The dict object for the CUSTOMER.csv can look like this after extracting usefull customer data:

        {
        'CUSTOMER_CODE': ['CUST0000010231', 'CUST0000010235'],
        'FIRSTNAME': ['Maria', 'George'],
        'LASTNAME': ['Alba', 'Lucas']
        }
        
        :param filename: Path to csv file
        :type filename: str
        :param header: Header (title) of the input csv file.
        :type filename: list
        :param target: list with ids to extract
        :type target: list
        '''
        if filename is None:
            raise ValueError("File name cannot be none.")
        csv_file = open(filename, encoding='utf-8')

        # initialize dict to store data  
        dict_keys = header
        data_dict = {key: [] for key in dict_keys}

        for line in csv_file:
            line = unidecode(line).replace('"', '').strip()

            fields = line.split(',')
            if fields[0] in target:
                for i, key in enumerate(header):
                    data_dict[key].append(fields[i])


        csv_file.close()
        return data_dict

    def to_csv(self, data_dict, output_filename):
        '''
        Takes as input extracted data as dict object, and writes them to .csv file.
        :param data_dict: dict object with data to export to csv
        :type: dict
        :param outputfilename: path to output file
        :type: str
        '''

        if output_filename is None:
            raise ValueError("File name cannot be none.")
        output_file = open(output_filename, 'w')

        header = list(data_dict.keys())

        # writes header 
        for i in range(len(header)):
            if i == len(header) - 1:
                output_file.write('%s\n' % header[i])
            else:
                output_file.write('%s,' % header[i])

        for idx, _ in enumerate(data_dict[header[0]]):

            # checks which dict we want to convert to csv to use the specified data type for each field.
            if header == cs.CUSTOMER_HEADER:
                output_file.writelines('%s,%s,%s\n' % (
                data_dict['CUSTOMER_CODE'][idx], data_dict['FIRSTNAME'][idx], data_dict['LASTNAME'][idx]))
            elif header == cs.INVOICE_HEADER:
                output_file.writelines('%s,%s,%f,%s\n' % (
                data_dict['CUSTOMER_CODE'][idx], data_dict['INVOICE_CODE'][idx], float(data_dict['AMOUNT'][idx]),
                data_dict['DATE'][idx]))
            elif header == cs.INVOICE_ITEM_HEADER:
                output_file.writelines('%s,%s,%f,%d\n' % (
                data_dict['INVOICE_CODE'][idx], data_dict['ITEM_CODE'][idx], float(data_dict['AMOUNT'][idx]),
                int(data_dict['QUANTITY'][idx])))

        output_file.close()


if __name__ == "__main__":
    f = FileHandler(cs.SAMPLE_PATH)
    test_customers = f.test_customers
    customer_dict = f.join(cs.CUSTOMER_PATH, cs.CUSTOMER_HEADER, test_customers)
    invoice_dict = f.join(cs.INVOICE_PATH, cs.INVOICE_HEADER, test_customers)
    invoice_item_dict = f.join(cs.INVOICE_ITEM_PATH, cs.INVOICE_ITEM_HEADER, invoice_dict['INVOICE_CODE'])

    f.to_csv(customer_dict, cs.CUSTOMER_OUT)
    f.to_csv(invoice_dict, cs.INVOICE_OUT)
    f.to_csv(invoice_item_dict, cs.INVOICE_ITEM_OUT)
