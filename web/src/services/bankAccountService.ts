import { apiClient } from "../api/config";
import { BankAccount, CreateBankAccountDto } from "../types/bankAccount";

const BASE_PATH = "/bankaccounts";

export const bankAccountService = {
  getAll: async (): Promise<BankAccount[]> => {
    const response = await apiClient.get(BASE_PATH);
    return response.data.bankaccounts;
  },

  getById: async (id: number): Promise<BankAccount> => {
    const response = await apiClient.get(`${BASE_PATH}/${id}`);
    return response.data;
  },

  create: async (data: CreateBankAccountDto): Promise<BankAccount> => {
    const response = await apiClient.post(BASE_PATH, {
      bankaccounts: [data],
    });
    return response.data.bankaccounts[0];
  },

  update: async (
    id: number,
    data: Partial<CreateBankAccountDto>
  ): Promise<BankAccount> => {
    const response = await apiClient.post(BASE_PATH, {
      bankaccounts: [{ ...data, id }],
    });
    return response.data.bankaccounts[0];
  },

  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`${BASE_PATH}/${id}`);
  },
};
