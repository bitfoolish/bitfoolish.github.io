
import { NavDropdown, Container, Nav, Navbar } from "react-bootstrap";
import { Link } from "react-router-dom";
function NavbarTop() {
    return (
      <>
      <Navbar bg="light" expand="lg">
        <Container>
        <Nav.Link href="/" activeClassName="active"> Home </Nav.Link>
        <Nav.Link as={Link} to="/projects" activeClassName="active"> Projects </Nav.Link>
        </Container>
      </Navbar>
      </>
    );
  }
  
  export default NavbarTop;