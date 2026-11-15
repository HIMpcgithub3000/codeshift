package com.codeshift;

import com.codeshift.model.Owner;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;

import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Owner Entity Behavioral Unit Tests")
public class OwnerTest {

    private Owner owner;

    @BeforeEach
    void setUp() {
        owner = new Owner("101", "George", "Franklin", "110 W. Liberty St.", "Madison", "6085551023");
    }

    @Test
    @DisplayName("Verify Owner attributes initialization")
    void testOwnerAttributes() {
        assertEquals("101", owner.getId());
        assertEquals("George", owner.getFirstName());
        assertEquals("Franklin", owner.getLastName());
        assertEquals("6085551023", owner.getTelephone());
        assertNotNull(owner.getCity());
    }

    @Test
    @DisplayName("Verify Owner full name derivation")
    void testOwnerFullName() {
        assertEquals("George Franklin", owner.getFullName());
    }

    @Test
    @DisplayName("Verify Owner equality contract")
    void testOwnerEquality() {
        Owner owner2 = new Owner("101", "George", "Franklin", "110 W. Liberty St.", "Madison", "6085551023");
        assertEquals(owner, owner2);
        assertTrue(owner.toString().contains("George"));
    }
}

