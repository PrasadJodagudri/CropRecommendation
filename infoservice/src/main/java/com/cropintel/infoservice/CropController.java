package com.cropintel.infoservice;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;
import java.util.Map;
import java.util.Optional;

@RestController
@CrossOrigin(origins = "http://127.0.0.1:5500") // Or "*" for testing, but specific is better
public class CropController {

    // This dataset has been updated with fully verified and working image URLs.
    private static final Map<String, CropInfo> CROP_DATA = Map.ofEntries(
        Map.entry("rice", new CropInfo("Rice", "A staple food for over half of the world's population, grown in flooded paddies.", "images/rice.jpg", "Kharif (June-July)", "High")),
        Map.entry("maize", new CropInfo("Maize (Corn)", "A versatile cereal grain used for human consumption, animal feed, and biofuel.", "images/maize.jpg", "Kharif (June-July)", "Moderate")),
        Map.entry("chickpea", new CropInfo("Chickpea", "A legume known for its nutty taste and high protein content, a key ingredient in hummus.", "images/chickpea.jpg", "Rabi (October-November)", "Low")),
        Map.entry("kidneybeans", new CropInfo("Kidney Beans", "A variety of the common bean, named for its shape. Rich in protein and fiber.","images/kidneybeans.jpg", "Kharif / Rabi", "Moderate")),
        Map.entry("pigeonpeas", new CropInfo("Pigeon Peas", "A perennial legume, also known as Arhar or Toor dal. It is a major source of protein in India.", "images/pigeonpeas.jpg", "Kharif (June-July)", "Low")), // <-- VERIFIED NEW URL
        Map.entry("mothbeans", new CropInfo("Moth Beans", "A drought-resistant legume, commonly grown in arid and semi-arid regions of India.", "images/mothbeans.jpg", "Kharif (July-August)", "Very Low")),
        Map.entry("mungbean", new CropInfo("Mung Bean", "A small, green bean used in both savory and sweet dishes. It's a fast-growing warm-season legume.", "images/mungbean.jpg", "Kharif / Zaid", "Low")),
        Map.entry("blackgram", new CropInfo("Black Gram", "Also known as Urad dal, it's a highly prized pulse, rich in protein and dietary fiber.", "images/blackgram.jpg", "Kharif (June-July)", "Low")),
        Map.entry("lentil", new CropInfo("Lentil", "A type of pulse, known for its lens-shaped seeds. It is a staple food, providing protein and fiber.", "images/lentil.jpg", "Rabi (October-November)", "Low")),
        Map.entry("pomegranate", new CropInfo("Pomegranate", "A fruit-bearing deciduous shrub, known for its jewel-like seeds (arils) that are rich in antioxidants.", "images/pomegranate.jpg", "Year-round", "Low")),
        Map.entry("banana", new CropInfo("Banana", "An elongated, edible fruit, botanically a berry. It is a major fruit crop grown in tropical and subtropical areas.", "images/banana.jpg", "Year-round", "High")),
        Map.entry("mango", new CropInfo("Mango", "A tropical stone fruit, known as the 'king of fruits'. It's celebrated for its sweet taste and fragrance.", "images/mango.jpg", "June-July", "Moderate")),
        Map.entry("grapes", new CropInfo("Grapes", "A fruit, botanically a berry, that grows in clusters on vines. Used for making wine, juice, and raisins.", "images/grapes.jpg", "October-January", "Moderate")),
        Map.entry("watermelon", new CropInfo("Watermelon", "A large, sweet fruit of the gourd family, with a green rind and watery, red flesh.", "images/watermelon.jpg", "Summer (Feb-March)", "High")),
        Map.entry("muskmelon", new CropInfo("Muskmelon", "A species of melon that has been developed into many cultivated varieties, known for its sweet, musky aroma.", "images/muskmelon.jpg", "Summer (Feb-March)", "Moderate")),
        Map.entry("apple", new CropInfo("Apple", "A pome fruit, one of the most widely cultivated tree fruits. Known for its crisp texture and varied sweetness.","images/apple.jpg", "December-February", "Moderate")),
        Map.entry("orange", new CropInfo("Orange", "A citrus fruit known for its high vitamin C content, with a tough, shiny orange skin and juicy inner flesh.", "images/orange.jpg", "Monsoon / Spring", "Moderate")),
        Map.entry("papaya", new CropInfo("Papaya", "A tropical fruit with a sweet taste and vibrant color. The flesh is rich in vitamins and minerals.", "images/papaya.jpg", "Feb-Mar / Jun-Oct", "Low")),
        Map.entry("coconut", new CropInfo("Coconut", "Grown on a large palm tree, the coconut has many culinary and non-culinary uses.", "images/coconut.jpg", "Year-round", "High")),
        Map.entry("cotton", new CropInfo("Cotton", "A soft, fluffy staple fiber that grows in a boll. It is the most widely used natural fiber for textiles.", "images/cotton.jpg", "Kharif (April-June)", "Moderate")),
        Map.entry("jute", new CropInfo("Jute", "A long, soft, shiny bast fiber that can be spun into coarse, strong threads. Also known as the 'Golden Fibre'.","images/jute.jpg", "March-May", "High")),
        Map.entry("coffee", new CropInfo("Coffee", "A brewed drink prepared from roasted coffee beans, the seeds of berries from certain flowering plants.", "images/coffee.jpg", "Monsoon (June-July)", "High"))
    );

    @GetMapping("/api/crop-info/{cropName}")
    public CropInfo getCropInfo(@PathVariable String cropName) {
        return Optional.ofNullable(CROP_DATA.get(cropName.toLowerCase())).orElse(new CropInfo());
    }
}

