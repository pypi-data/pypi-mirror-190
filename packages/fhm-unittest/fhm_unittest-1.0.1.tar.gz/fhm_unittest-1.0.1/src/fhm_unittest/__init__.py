from fuzzywuzzy import fuzz
def output_test(returned_output, expected_output):
  score = fuzz.WRatio(returned_output, expected_output)
  if score == 100:
    print("Accepted")
  # elif score >= 90:
  #   print(f'Accepted [{score}%]')
  elif score >= 50:
    print(f'Not Accepted [Your output: {returned_output}  |  Expected Output: {expected_output}]')
  else:
    print(f"Wrong Answer [Your output: {returned_output}  |  Expected Output: {expected_output}]")