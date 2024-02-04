import org.springframework.web.bind.annotation.*;
import org.springframework.beans.factory.annotation.Autowired;

@RestController
public class UserController {

    @Autowired
    private UserService userService; // Assume this service contains logic for interacting with BigQuery

    @Autowired
    private EmailService emailService;

    @GetMapping("/user/{username}")
    public UserDetails getUser(@PathVariable String username) {
        // Fetch user details from BigQuery
        UserDetails userDetails = userService.getUserDetails(username);
        return userDetails;
    }

    @PostMapping("/book")
    public String bookChildcare(@RequestBody BookingRequest bookingRequest) {
        // Implement booking logic, including sending confirmation emails
        // You might need a BookingService for detailed booking operations
        emailService.sendEmail(bookingRequest.getUserEmail(), "Your GoMama Booking is Confirmed", "Booking details...");
        return "Booking confirmed";
    }

    // Implement other endpoints as needed
}
