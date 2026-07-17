package com.raphdev.accountmanager.model;

import java.util.Random;

public class Category {
    private String name;
    private String color;

    public Category(String name) {
        this(name, new Random());
    }

    Category(String name, Random random) {
        this.name = name;
        int nextInt = random.nextInt(0xffffff + 1);
        this.color = String.format("#%06x", nextInt);
    }

    public Category(String name, String color) {
        if (color == null || !color.matches("^#[0-9a-fA-F]{6}$")) {
            throw new IllegalArgumentException("Invalid color format");
        }

        this.name = name;
        this.color = color.toLowerCase();
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getColor() {
        return color;
    }

    public void setColor(String color) {
        if (color == null || !color.matches("^#[0-9a-fA-F]{6}$")) {
            throw new IllegalArgumentException("Invalid color format");
        }
        this.color = color.toLowerCase();
    }
}
