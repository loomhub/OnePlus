import { useEffect, useState } from "react";
import { BankAccount } from "../../types/bankAccount";
import { bankAccountService } from "../../services/bankAccountService";

interface BankAccountListProps {
  onEdit: (account: BankAccount) => void;
  onRefresh?: () => void;
  refreshKey?: number;
}

export const BankAccountList = ({
  onEdit,
  onRefresh,
  refreshKey = 0,
}: BankAccountListProps) => {
  const [bankAccounts, setBankAccounts] = useState<BankAccount[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchBankAccounts();
  }, [refreshKey]);

  const fetchBankAccounts = async () => {
    try {
      setLoading(true);
      const accounts = await bankAccountService.getAll();
      setBankAccounts(accounts);
      setError(null);
    } catch (err) {
      setError("Failed to fetch bank accounts");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await bankAccountService.delete(id);
      setBankAccounts((accounts) =>
        accounts.filter((account) => account.id !== id)
      );
      setError(null);
    } catch (err) {
      setError("Failed to delete bank account");
      console.error(err);
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  return (
    <div className="bank-account-list">
      <h2>Bank Accounts</h2>
      <table>
        <thead>
          <tr>
            <th>Bank Account Key</th>
            <th>Bank</th>
            <th>Account Type</th>
            <th>Account Number</th>
            <th>LLC</th>
            <th>Property Name</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {bankAccounts.map((account) => (
            <tr key={account.bank_account_key}>
              <td>{account.bank_account_key}</td>
              <td>{account.bank}</td>
              <td>{account.account_type}</td>
              <td>{account.account_number}</td>
              <td>{account.llc}</td>
              <td>{account.property_name || "-"}</td>
              <td>
                <button onClick={() => onEdit(account)}>Edit</button>
                <button onClick={() => handleDelete(account.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
