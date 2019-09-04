    @Story("Verify ...")
    @Test(groups = {"test"})
    public void what() throws Exception{

//        List<String> book = readFile("C:\\Users\\rodions\\projects\\zohar\\zohar\\testfile.txt");
//        List<String> book = readFile("C:\\Users\\rodions\\projects\\zohar\\zohar\\lib1\\12. Зоhар Ваигаш (135).txt");
        String targetFile = "C:\\Users\\rodions\\projects\\zohar\\zohar\\lib1\\Бахир.txt";
        BufferedReader file = new BufferedReader(new FileReader(targetFile));
        StringBuffer inputBuffer = new StringBuffer();
        String line;

        while ((line = file.readLine()) != null) {
            Pattern word = Pattern.compile("[א-ת]+");
            Matcher match = word.matcher(line);
            int occur = 0;

            while (match.find()) {
//                System.out.println(line.charAt(match.start()-1+occur));
                if (line.charAt(match.start()-1+occur) != ' '){
                    if (line.charAt(match.start()-1+occur) != '[') {
                        if (line.charAt(match.start()-1+occur) != '(') {
                            System.out.println("Need to add space after " + (match.start() - 1));
                            System.out.println("Before: " + line);
                            line = line.substring(0, (match.start() + occur)) + " " + line.substring((match.start() + occur), line.length());
                            System.out.println("After:  " + line);
                            occur += 1;
                        }
                    }
                }
            }
            inputBuffer.append(line);
            inputBuffer.append('\n');
        }
        file.close();

        FileOutputStream fileOut = new FileOutputStream(targetFile);
        fileOut.write(inputBuffer.toString().getBytes());
        fileOut.close();
    }