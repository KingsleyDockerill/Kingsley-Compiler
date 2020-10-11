// Output num program

main()
{
    auto a = 5;
    auto b = 6;
    auto c = "Hello, world!";
    auto d = 'This';
    auto e = ' is ';
    auto f = 'putc';
    auto g = 'har*n';
    auto h = ""; // This assigns h as nothing so it will be equal to input
    putnumb(&a);
    putnumb(b);
    putstr(c);
    putchar(d);
    putchar(e);
    putchar(f);
    putchar(g);
    getstr(h);
    putstr(h);
}