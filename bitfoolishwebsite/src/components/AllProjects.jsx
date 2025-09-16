import { useState, useEffect } from "react";
import { Button, Col, Row } from "react-bootstrap";
import { Link } from "react-router-dom";
function AllProjects(){

    const projects = [
        {
            title: "Kris Kindle",
            description: "This project was coded in python. It randomises the entered names, creates deranged pairs, emails each gifter with their giftee",
            link: "https://github.com/bitfoolish/KrisKindle"
        },
        {
            title: "Desktop Timer (Linux & Windows versions)",
            description: "This project was coded in python. It randomises the entered names, creates deranged pairs, emails each gifter with their giftee",
            link: "https://github.com/bitfoolish/desktopTimer"
        },
        {
            title: "This beautiful WebSite",
            description: "This project was created using primarily using React & Bootstrap.",
            link: "https://github.com/bitfoolish/bitfoolish.github.io"
        },
    ]

    return(
        <>
            <Row>
                {projects.map(({title, description, link}) => (

                <Col sm={4} className="mb-4"> 
                    <div className="border p-3 rounded"></div>
                    <h4>{title}</h4>
                    <Link to={link}>
                            <Button style={{ marginLeft:"1%" }}> Github Repo </Button>
                    </Link> <br/>
                    <p>{description}</p>
                    <hr/>
                </Col>
                ))}

</Row>
        </>
    )
}
export default AllProjects;
