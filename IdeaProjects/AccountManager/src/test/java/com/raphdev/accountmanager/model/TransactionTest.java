package com.raphdev.accountmanager.model;

import java.time.LocalDate;
import java.math.BigDecimal;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.*;

class TransactionTest {

    private Transaction transaction;

    @BeforeEach
    void setUp() {
        transaction = new Transaction(LocalDate.of(2026,10,20), "Grocery Purchase", BigDecimal.valueOf(30.0), new Category("Alimentary"), 0);
    }

    @Test
    void testTransactionGetters() {
        LocalDate date = LocalDate.of(2026, 10, 20);
        BigDecimal amount = new BigDecimal("30.00");

        assertEquals(date, transaction.getDate());
        assertEquals("Grocery Purchase", transaction.getLabel());
        assertEquals(new Category("Alimentary").getName(), transaction.getCategory().getName());
        assertEquals(0, transaction.getAccountId());

        assertEquals(0, amount.compareTo(transaction.getAmount()));
    }

    @Test
    void testTransactionSetters() {
        LocalDate date = LocalDate.of(2026, 10, 20);
        String label = "Steam Purchase";
        BigDecimal amount = new BigDecimal("30.00");
        Category category = new Category("Games");

        transaction.setDate(date);
        transaction.setLabel(label);
        transaction.setAmount(amount);
        transaction.setCategory(category);

        assertEquals(date, transaction.getDate());
        assertEquals(label, transaction.getLabel());
        assertEquals(amount, transaction.getAmount());
        assertEquals(category, transaction.getCategory());
    }

    @Test
    void testTransactionInvalidAmount() {
        assertThrows(IllegalArgumentException.class, () -> transaction.setAmount(null));
        assertThrows(IllegalArgumentException.class, () -> transaction.setAmount(BigDecimal.ZERO));
        assertThrows(IllegalArgumentException.class, () -> transaction = new Transaction(LocalDate.of(2026,10,20), "Grocery Purchase", null, new Category("Alimentary"), 0));
        assertThrows(IllegalArgumentException.class, () -> transaction = new Transaction(LocalDate.of(2026,10,20), "Grocery Purchase", BigDecimal.ZERO, new Category("Alimentary"), 0));
    }

    @Test
    void testTransactionInvalidLabel() {
        assertThrows(IllegalArgumentException.class, () -> transaction.setLabel(null));
        assertThrows(IllegalArgumentException.class, () -> transaction.setLabel(""));

        transaction = new Transaction(LocalDate.of(2026,10,20), "", BigDecimal.valueOf(30.0), new Category("Alimentary"), 0);
        assertEquals("Undefined", transaction.getLabel());
        transaction = new Transaction(LocalDate.of(2026,10,20), null, BigDecimal.valueOf(30.0), new Category("Alimentary"), 0);
        assertEquals("Undefined", transaction.getLabel());

    }
    @Test
    void testTransactionInvalidCategory() {
        assertThrows(IllegalArgumentException.class, () -> transaction.setCategory(null));
        assertThrows(IllegalArgumentException.class, () -> transaction.setCategory(new Category("")));

        transaction = new Transaction(LocalDate.of(2026,10,20), "Grocery Purchase", BigDecimal.valueOf(30.0), null, 0);
        assertEquals("Undefined", transaction.getCategory().getName());
        transaction = new Transaction(LocalDate.of(2026,10,20), "Grocery Purchase", BigDecimal.valueOf(30.0), new Category(""), 0);
        assertEquals("Undefined", transaction.getCategory().getName());

    }

}