from pydantic import BaseModel, field_validator, ValidationError

class Patient(BaseModel):

    def __init__(self,first_name,last_name,ssn):
        self.first_name = first_name
        self.last_name = last_name
        self.ssn = ssn

    @field_validator('ssn')
    @classmethod
    def validate_ssn(cls, v: str) -> str:
        if len(v) != 15:
            raise ValueError('Social security number must be 15 digits long')

        # Validate first digit
        if v[0] not in ['1', '2']:
            raise ValueError('First digit must be 1 or 2')

        # Validate birth month
        birth_month = int(v[3:5])
        if birth_month < 1 or birth_month > 12:
            raise ValueError('Birth month must be between 01 and 12')


        # # Validate checksum
        # checksum = int(v[13:15])
        # expected_checksum = (int(v[:13]) % 97) % 100
        # if checksum != expected_checksum:
        #     raise ValueError('Invalid checksum')

        return v