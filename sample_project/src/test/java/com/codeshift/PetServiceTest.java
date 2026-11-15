package com.codeshift;

import com.codeshift.model.Pet;
import com.codeshift.repository.PetRepository;
import com.codeshift.service.PetService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
@DisplayName("PetService Isolated Unit Tests with Mockito")
public class PetServiceTest {

    @Mock
    private PetRepository petRepository;

    @InjectMocks
    private PetService petService;

    private Pet samplePet;

    @BeforeEach
    void setUp() {
        samplePet = new Pet("1", "Leo", "cat", 2);
    }

    @Test
    @DisplayName("Verify findById delegates to repository")
    void testFindById() {
        when(petRepository.findById("1")).thenReturn(Optional.of(samplePet));

        Optional<Pet> found = petService.findById("1");
        assertTrue(found.isPresent());
        assertEquals("Leo", found.get().getName());
        verify(petRepository, times(1)).findById("1");
    }

    @Test
    @DisplayName("Verify findAll retrieves list of pets")
    void testFindAll() {
        List<Pet> pets = Arrays.asList(samplePet, new Pet("2", "Basil", "hamster", 1));
        when(petRepository.findAll()).thenReturn(pets);

        List<Pet> result = petService.findAll();
        assertEquals(2, result.size());
        verify(petRepository, times(1)).findAll();
    }

    @Test
    @DisplayName("Verify save persists pet through repository")
    void testSave() {
        when(petRepository.save(samplePet)).thenReturn(samplePet);

        Pet saved = petService.save(samplePet);
        assertNotNull(saved);
        assertEquals("Leo", saved.getName());
        verify(petRepository, times(1)).save(samplePet);
    }
}

