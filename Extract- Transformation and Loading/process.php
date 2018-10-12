<?php
$servername = "database_server";
$username = "username";
$password = "password";

if ( isset($_POST['submit']) ) {
  $sql = $_POST["SQL"];
  $con = mysqli_connect($servername, $username, $password);
  if (mysqli_connect_errno())
  {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }
  else{
      echo "successful connection";
      echo "<br>";
       mysqli_query($con, "SET profiling = 1;");
      $result=mysqli_store_result($con);
      mysqli_free_result($result);

    if (mysqli_multi_query($con,$sql))
    {
        echo"query successed";
        echo "<br>";
      do
        {
        // Store first result set
        if ($result=mysqli_store_result($con)) {
          // Fetch one and one row
          while ($row=mysqli_fetch_row($result))
            {
              $len=count($row);
              for ($i=0;$i<$len;$i++)
                   {printf("%s  ",$row[$i]);
                    if($i==$len-1) printf("<br>");}
            }
          // Free result set
          mysqli_free_result($result);
        }
        }
      while (mysqli_next_result($con));


  }
  else {echo "query failed";}

//profile
$resource = $con->query('SHOW PROFILES');
while ( $rows = $resource->fetch_assoc() ) {
  print_r($rows);
  printf("<br>");
//echo "{$row['field']}";
   }


}//successful connection

mysqli_close($con);
}// user input
?>
