export interface BankAccount {
  id: number;
  bank_account_key: string;
  bank: string;
  account_type: string;
  account_number: string;
  llc: string;
  property_name: string | null;
}

export interface CreateBankAccountDto {
  bank_account_key: string;
  bank: string;
  account_type: string;
  account_number: string;
  llc: string;
  property_name?: string;
}
