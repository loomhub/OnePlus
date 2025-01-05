import { useState } from "react";
import { CreateBankAccountDto } from "../../types/bankAccount";

interface BankAccountFormProps {
  initialData?: Partial<CreateBankAccountDto>;
  onSubmit: (data: CreateBankAccountDto) => Promise<void>;
  onCancel: () => void;
}

export const BankAccountForm = ({
  initialData = {},
  onSubmit,
  onCancel,
}: BankAccountFormProps) => {
  const [formData, setFormData] = useState<CreateBankAccountDto>({
    bank_account_key: initialData.bank_account_key || "",
    bank: initialData.bank || "",
    account_type: initialData.account_type || "",
    account_number: initialData.account_number || "",
    llc: initialData.llc || "",
    property_name: initialData.property_name || "",
  });

  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await onSubmit(formData);
      setError(null);
    } catch (err) {
      setError("Failed to save bank account");
      console.error(err);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bank-account-form">
      {error && <div className="error">{error}</div>}

      <div className="form-group">
        <label htmlFor="bank_account_key">Bank Account Key:</label>
        <input
          type="text"
          id="bank_account_key"
          name="bank_account_key"
          value={formData.bank_account_key}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="bank">Bank:</label>
        <input
          type="text"
          id="bank"
          name="bank"
          value={formData.bank}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="account_type">Account Type:</label>
        <input
          type="text"
          id="account_type"
          name="account_type"
          value={formData.account_type}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="account_number">Account Number:</label>
        <input
          type="text"
          id="account_number"
          name="account_number"
          value={formData.account_number}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="llc">LLC:</label>
        <input
          type="text"
          id="llc"
          name="llc"
          value={formData.llc}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="property_name">Property Name:</label>
        <input
          type="text"
          id="property_name"
          name="property_name"
          value={formData.property_name}
          onChange={handleChange}
        />
      </div>

      <div className="form-actions">
        <button type="submit">Save</button>
        <button type="button" onClick={onCancel}>
          Cancel
        </button>
      </div>
    </form>
  );
};
