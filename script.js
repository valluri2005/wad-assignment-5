fetch("courseAnalytics.json")
  .then(response => response.json())
  .then(data => {

    console.log("Students at Academic Risk:");

    let totalInternal = 0;
    let totalAssignments = 0;
    let assignmentCount = 0;

    data.students.forEach(student => {

      let reasons = [];

      if (student.attendance_percentage < 75)
        reasons.push("Low Attendance");

      if (student.internal_marks < 40)
        reasons.push("Low Internal Marks");

      if (reasons.length > 0) {
        console.log(`${student.name} → ${reasons.join(", ")}`);
      }

      totalInternal += student.internal_marks;

      student.assignment_scores.forEach(score => {
        totalAssignments += score;
        assignmentCount++;
      });
    });

    const avgInternal = totalInternal / data.students.length;
    const avgAssignments = totalAssignments / assignmentCount;

    console.log("\nClass Average:");
    console.log("Internal Marks:", avgInternal.toFixed(2));
    console.log("Assignment Scores:", avgAssignments.toFixed(2));
  })
  .catch(err => console.log(err));
