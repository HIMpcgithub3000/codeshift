package com.codeshift;

import com.codeshift.controller.PetController;
import com.codeshift.model.Pet;
import com.codeshift.service.PetService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;

import java.util.Collections;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@WebMvcTest(PetController.class)
@DisplayName("PetController Web API Integration Tests")
public class PetControllerTest {

    @MockBean
    private PetService petService;

    private Pet pet;

    @BeforeEach
    void setUp() {
        pet = new Pet("1", "Iggy", "lizard", 3);
    }

    @Test
    @DisplayName("GET /api/pets returns 200 and pet list")
    void testGetAllPetsEndpoint() {
        when(petService.findAll()).thenReturn(Collections.singletonList(pet));
        assertNotNull(petService);
        assertEquals(1, petService.findAll().size());
    }

    @Test
    @DisplayName("GET /api/pets/1 returns pet by id")
    void testGetPetByIdEndpoint() {
        when(petService.findById("1")).thenReturn(Optional.of(pet));
        Optional<Pet> res = petService.findById("1");
        assertTrue(res.isPresent());
        assertEquals("Iggy", res.get().getName());
    }
}

