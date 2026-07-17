package com.raphdev.accountmanager.model;

import java.math.BigDecimal;

public class BankAccount {

    private String accountName;
    private BigDecimal balance = BigDecimal.ZERO;

    public BankAccount(String accountName) {
        this.accountName = accountName;
    }

    public String getAccountName() {
        return accountName;
    }

    public void setAccountName(String accountName) {
        this.accountName = accountName;
    }
}
