package com.raphdev.accountmanager.model;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

import java.util.Random;

class CategoryTest {

    @Test
    void testCategoryRandomColorExpression() {
        Random randomSeeded = new Random(123);
        Category cat = new Category("Grocery", randomSeeded);

        assertEquals("#b921f1", cat.getColor());
    }

    @Test
    void testCategoryConstructorWithOnlyName() {
        Category cat = new Category("Courses");

        // On vérifie que les propriétés sont initialisées
        assertNotNull(cat.getName());
        assertEquals("Courses", cat.getName());
    }

    @Test
    void testCategoryGetters() {
        Category cat = new Category("Games", "#1A2B3C");

        assertEquals("Games", cat.getName());
        assertEquals("#1a2b3c", cat.getColor());
    }

    @Test
    void testCategorySetters() {
        Category cat = new Category("Games", "#1a2b3c");

        cat.setName("Grocery");
        cat.setColor("#2b3c4d");

        assertEquals("Grocery", cat.getName());
        assertEquals("#2b3c4d", cat.getColor());
    }

    @Test
    void testCategoryConstructorInvalidColor() {
        // Ici, pas de problème : on teste une création qui échoue
        assertThrows(IllegalArgumentException.class, () -> new Category("Grocery", "Wrong Format"));
        assertThrows(IllegalArgumentException.class, () -> new Category("Grocery", (String) null));
    }

    @Test
    void testCategorySetColorInvalid() {
        Category cat = new Category("Games", "#1a2b3c");

        assertThrows(IllegalArgumentException.class, () -> cat.setColor("Wrong Format"));
        assertThrows(IllegalArgumentException.class, () -> cat.setColor(null));
    }
}