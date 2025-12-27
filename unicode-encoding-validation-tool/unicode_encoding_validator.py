# Author: Patrick Godinez
# 
# Description:
#   Unicode Encoding Validation Tool
#
#
#   Validates encoding and decoding behavior across multiple character encodings
#   with error handling and structured output.   
#    
#   Generate a random 10 character string using Chinese-Japanese-Korean characters
#   We encode and decode the generated string using different encoding scheme

import random
import binascii

#this function serves to create the random string with Chinese-Japanese-Korean char
def generate_CJK_str(length=10):
    try:
        #build the random string using the Chinese-Japanese-Korean characters
        return ''.join(chr(random.randint(0x4E00, 0x9FFF)) for _ in range(length))
    
    # handle error
    except Exception as e:
        print(f"[Error] String not generated: {e}")
        return ""

# function designed to encode the generated string using the different encoding schemes
def encoding_test(text):
    encodings = ["ascii", "latin-1", "cp1252", "utf-8", "utf-16", "utf-32"]
    results = {}

    print("\n=== Encode Test Results ===")
    for encoding in encodings:
        try:
            #here we try to encode the generated string into bytes for the given encoding
            encoded_bytes = text.encode(encoding)
            results[encoding] =encoded_bytes
            print(f"{encoding:<8} | SUCCESS | Bytes Length: {len(encoded_bytes)}")

        # handles errors for characters that cannot be encoded    
        except UnicodeEncodeError as err:
            print(f"{encoding:<8} | FAIL    | {err.__class__.__name__}: {err.reason}")
        
        # handle all other errors
        except Exception as err:

            print(f"{encoding:<8} | FAIL     | Unexpected error: {err}")
    
    # return dictionary of successful encodings
    return results

# function to take encdoded bytes and decode
def decode_str(encoding_results):

    encodings = ["ascii", "latin-1", "cp1252", "utf-8", "utf-16", "utf-32"]

    # print the table header
    print("\n=== Decode Test Results ===")
    header = f"{'Wencode':<10}{'REncode':<10}{'Bytes':<8}{'Chars':<8}{'Status':<10}{'Detail'}"
    print(header)
    print("-" * len(header))

    # here we are iterating through each successful written encoding 
    for write_encode, data in encoding_results.items():
        # here we try to decode the encoded bytes
        for read_encode in encodings:
            try:
                # decode with current "read" encoding
                decoded_text = data.decode(read_encode)
                status = "SUCCESS"
                detail = decoded_text[:8]
                print(f"{write_encode:<10}{read_encode:<10}{len(data):<8}{len(decoded_text):<8}{status:<10}{detail}")
            
            # handle decoding errors such as range issues, invalid bytes, etc
            except UnicodeDecodeError as err:
                status = "FAIL"
                detail = f"{err.__class__.__name__}: {err.reason}"

                print(f"{write_encode:<10}{read_encode:<10}{len(data):<8}{'-':<8}{status:<10}{detail}")
            
            # hanlde all other errors
            except Exception as err:
               status = "FAIL"
               detail = f"{type(err).__name__}: {err}"

               print(f"{write_encode:<10}{read_encode:<10}{len(data):<8}{'-':<8}{status:<10}{detail}")


# build main function to run program
def main():
    # generate the random CJK char
    cjk_str = generate_CJK_str()
    print("Random CJK String: ", cjk_str)
    print("Length Verification: ", len(cjk_str))

    # here we encode the result of the generated CJK string
    encoding_results = encoding_test(cjk_str)

    # here we decode the encoding_results using all cncoding types. 
    decode_str(encoding_results)

    print("\n Program completed successfully!")

if __name__ == "__main__":
    main()
