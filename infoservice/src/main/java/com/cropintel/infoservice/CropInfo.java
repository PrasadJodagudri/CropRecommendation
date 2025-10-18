package com.cropintel.infoservice;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class CropInfo {
    private String name;
    private String description;
    private String imageUrl;
    private String sowingSeason;
    private String waterNeeds;
}