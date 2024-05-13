import boto3
import json
import itertools

def generate_vanity_numbers(phone_number):
    key_map = {
        '2': 'ABC', '3': 'DEF', '4': 'GHI', '5': 'JKL',
        '6': 'MNO', '7': 'PQRS', '8': 'TUV', '9': 'WXYZ'
    }
    last_four = phone_number[-4:]
    possible_combinations = []
    for digit in last_four:
        if digit in key_map:
            possible_combinations.append(key_map[digit])
        else:
            possible_combinations.append([''])  # Make sure it's a list with a placeholder
    all_combinations = list(itertools.product(*possible_combinations))
    all_combinations = [''.join(comb) for comb in all_combinations]
    best_five = all_combinations[:5] if len(all_combinations) > 5 else all_combinations
    print("Best five combinations:", best_five)
    return best_five

def save_to_dynamodb(phone_number, vanity_numbers):
    dynamodb = boto3.resource('dynamodb',region_name = 'us-east-1')
    table = dynamodb.Table('VanityNumbers')
    try:
        table.put_item(
            Item={
                'PhoneNumber': phone_number,
                'VanityNumbers': vanity_numbers
            }
        )
    except Exception as e:
        print("Error saving to DynamoDB:", e)
        raise e  # Reraising the exception

def lambda_handler(event, context):
    try:
        phone_number = event['phone_number']
        vanity_numbers = generate_vanity_numbers(phone_number)
        print(vanity_numbers)
        save_to_dynamodb(phone_number, vanity_numbers)
        return {
            'statusCode': 200,
            'body': json.dumps({
                'original': phone_number,
                'best vanity numbers': vanity_numbers
            })
        }
    except KeyError:
        return {'statusCode': 400, 'body': 'Missing phone number'}
    except Exception as e:
        return {'statusCode': 500, 'body': str(e)}

# This should be the last part of your script, especially if this script is meant to be imported or used elsewhere.
if __name__ == "__main__":
    # Test event based on the JSON structure
    # Function call to simulate the Lambda invocation
    result = lambda_handler(test_event, None)
    # Print the output which includes the status code and body
    print(result)
