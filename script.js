fetch('students.json')
  .then(response => response.json())
  .then(data => {
    const filteredStudents = data.filter(student => student.cgpa > 8.0);

    console.log("Students with CGPA > 8.0:");
    filteredStudents.forEach(student => {
      console.log(`${student.name} (${student.department}) - CGPA: ${student.cgpa}`);
    });
  })
  .catch(error => console.error("Error:", error));
