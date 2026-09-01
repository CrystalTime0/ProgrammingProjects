package com.raphdev.accountmanager.model;

import java.time.LocalDate;
import java.math.BigDecimal;



/**
 * Represents a financial transaction associated with an account.
 * <p>
 * A transaction is defined by a date, a descriptive label, an amount, and a category.
 * The amount must be non-null and different from zero. Positive amounts represent
 * credits, while negative amounts represent debits.
 * </p>
 */
public class Transaction {
    private LocalDate date; // YYYY-MM-DD
    private String label;
    private BigDecimal amount;
    private Category category;
    private int accountId;

    /**
     * Create a new Transaction
     *
     * @param date     The date of the transaction.
     * @param label    The label of the transaction.
     * @param amount   The amount of the transaction (positive for a credit, negative for a debit).
     * @param category The category of the transaction.
     *
     * @throws IllegalArgumentException if the amount is null or equal to 0
     */
    public Transaction(LocalDate date, String label, BigDecimal amount, Category category, int accountId) {
        if (amount == null) {
            throw new IllegalArgumentException("The Amount can't be null.");
        }
        if (amount.compareTo(BigDecimal.ZERO) == 0) {
            throw new IllegalArgumentException("The Amount can't be equal to 0.");
        }

        this.date = date;
        this.label = (label == null || label.isBlank()) ? "Undefined" : label;
        this.category = (category == null || category.getName().isBlank()) ? new Category("Undefined") : category;
        this.amount = amount;
        this.accountId = accountId;
    }

    public LocalDate getDate() {
        return date;
    }

    public void setDate(LocalDate date) {
        this.date = date;
    }

    public String getLabel() {
        return label;
    }

    public void setLabel(String label) {
        if (label == null || label.isBlank()) {throw new IllegalArgumentException("The Label can't be null or empty.");}
        this.label = label;
    }

    public BigDecimal getAmount() {
        return amount;
    }

    public void setAmount(BigDecimal amount) {
        if (amount == null) {
            throw new IllegalArgumentException("The Amount can't be null.");
        }
        if (amount.compareTo(BigDecimal.ZERO) == 0) {
            throw new IllegalArgumentException("The Amount can't be equal to 0.");
        }
        this.amount = amount;
    }

    public Category getCategory() {
        return category;
    }

    public void setCategory(Category category) {
        if (category == null || category.getName().isBlank()) {throw new IllegalArgumentException("The Category can't be null or empty.");}
        this.category = category;
    }

    public int getAccountId() {
        return accountId;
    }
}
