import { useState } from "react";
import { BankAccount, CreateBankAccountDto } from "../../types/bankAccount";
import { bankAccountService } from "../../services/bankAccountService";
import { BankAccountList } from "./BankAccountList";
import { BankAccountForm } from "./BankAccountForm";

export const BankAccountsPage = () => {
  const [showForm, setShowForm] = useState(false);
  const [selectedAccount, setSelectedAccount] = useState<BankAccount | null>(
    null
  );

  const [refreshKey, setRefreshKey] = useState(0);

  const handleCreateAccount = async (data: CreateBankAccountDto) => {
    await bankAccountService.create(data);
    setShowForm(false);
    setSelectedAccount(null);
    setRefreshKey((prev) => prev + 1);
  };

  const handleUpdateAccount = async (data: CreateBankAccountDto) => {
    if (selectedAccount) {
      await bankAccountService.update(selectedAccount.id, data);
      setShowForm(false);
      setSelectedAccount(null);
    }
  };

  const handleEdit = (account: BankAccount) => {
    setSelectedAccount(account);
    setShowForm(true);
  };

  const handleCancel = () => {
    setShowForm(false);
    setSelectedAccount(null);
  };

  return (
    <div className="bank-accounts-page">
      <div className="header">
        <h1>Bank Accounts</h1>
        {!showForm && (
          <button onClick={() => setShowForm(true)}>Add New Account</button>
        )}
      </div>

      {showForm ? (
        <BankAccountForm
          initialData={
            selectedAccount
              ? {
                  bank_account_key: selectedAccount.bank_account_key,
                  bank: selectedAccount.bank,
                  account_type: selectedAccount.account_type,
                  account_number: selectedAccount.account_number,
                  llc: selectedAccount.llc,
                  property_name: selectedAccount.property_name || undefined,
                }
              : {}
          }
          onSubmit={selectedAccount ? handleUpdateAccount : handleCreateAccount}
          onCancel={handleCancel}
        />
      ) : (
        <BankAccountList
          onEdit={handleEdit}
          onRefresh={() => setRefreshKey((prev) => prev + 1)}
        />
      )}
    </div>
  );
};
