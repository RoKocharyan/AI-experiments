This is user request: 
"@request"
Task:
Generate a YAML file named customization.yaml that follows the structure and rules outlined below.

Example of a Valid YAML File:

customization:
  - microservice:
      category: AccountMS
      model:
        - modelField: onboardingLink
          type: string
          uiElement: infocard
          friendlyName: Onboarding link
          content: url
        - modelField: manager
          type: string
          uiElement: infocard
          friendlyName: Manager
          content:
Rules and Requirements:

Root Structure:

The root key must be customization.
Under customization, there should be a list of microservice entries.
Microservice Level:

Required Keys:
category: Must be one of the following:
AccountMS
model: A list of model field entries.
Model Level:

Each entry under model must include the following required keys:
modelField: A string representing the name of the field.
type: Must be one of the following:
string
uiElement: Must be one of the following:
infocard
friendlyName: A string providing a user-friendly name for the field.
content: Must be one of the following:
url
text
Value Constraints:

Valid Categories:
AccountMS
Valid Types:
string
Valid UI Elements:
infocard
Valid Contents:
url
text
Key Presence:

Ensure all required keys are present at both the microservice and model levels.
No additional keys should be included beyond those specified.
Formatting:

Maintain proper YAML indentation and syntax.
Ensure that lists and nested objects are correctly structured.
Instructions:

Adherence: The generated YAML must strictly follow the structure and rules provided above.
Validation: Before finalizing, ensure that all values for category, type, uiElement, and content are within the specified valid options.
Completeness: All required keys must be present, and no required information should be omitted.
Example Reference: Use the provided example as a reference for formatting and structure, but populate it with different valid data as needed.
Objective:
Create a well-structured customization.yaml file that can be used for configuration purposes, ensuring consistency and validity according to the specified rules.

