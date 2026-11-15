package com.codeshift;

import com.codeshift.model.Pet;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;

import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Pet Entity Behavioral Unit Tests")
public class PetTest {

    private Pet pet;

    @BeforeEach
    void setUp() {
        pet = new Pet("1", "Fluffy", "Dog", 3);
    }

    @Test
    @DisplayName("Verify Pet getters and property state")
    void testPetProperties() {
        assertEquals("1", pet.getId());
        assertEquals("Fluffy", pet.getName());
        assertEquals("Dog", pet.getSpecies());
        assertEquals(3, pet.getAge());
        assertNotNull(pet.getId());
    }

    @Test
    @DisplayName("Verify Pet speak behavior based on species")
    void testPetSpeak() {
        Pet dog = new Pet("1", "Rex", "dog", 2);
        Pet cat = new Pet("2", "Whiskers", "cat", 4);
        Pet bird = new Pet("3", "Polly", "bird", 1);

        assertEquals("Woof!", dog.speak());
        assertEquals("Meow!", cat.speak());
        assertEquals("Hello!", bird.speak());
    }

    @Test
    @DisplayName("Verify equality and toString representation")
    void testEqualsAndToString() {
        Pet pet2 = new Pet("1", "Fluffy", "Dog", 3);
        assertEquals(pet, pet2);
        assertTrue(pet.toString().contains("Fluffy"));
        assertNotNull(pet.toString());
    }
}

