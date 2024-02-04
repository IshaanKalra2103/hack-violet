import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@SpringBootApplication
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

}

@Service
public class EmailService {

    @Autowired
    private JavaMailSender emailSender;

    public void sendEmail(String to, String subject, String text) {
        SimpleMailMessage message = new SimpleMailMessage();
        message.setFrom("goelparsh@gmail.com");
        message.setTo(to);
        message.setSubject(subject);
        message.setText(text);
        emailSender.send(message);
    }
}


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
}
