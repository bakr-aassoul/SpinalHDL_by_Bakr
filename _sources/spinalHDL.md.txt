# Einleitung

## Ziele dieser Dokumentation
Ziel dieser Dokumentation ist es, eine Einführung in SpinalHDL zu geben und die wichtigsten Grundlagen zu erklären.  
Dazu werden Praxisbeispiele vorgestellt, die den gesamten Entwicklungsprozess abdecken.  
Dazu gehören die Komponentenbeschreibung, die Simulation und schließlich die Generierung von Verilog- oder VHDL-Code.  
Neben diesem kleinen Projektbeispiel wird auch ein Beispiel zum komplexerem Design beschrieben.  
In unserem Fall ist dies der **VexRiscv-Prozessor**.


## Motivation
SpinalHDL ist eine moderne HDL (Hardwarebeschreibungssprache), die im Jahr 2014 eingeführt wurde und als Domain-Specific 
Language (DSL) in Scala implementiert ist.
Sie bietet die Möglichkeit, digitale Schaltungen zu entwerfen. Danach können diese als Verilog oder VHDL-Code generiert werden, der einsatzbereit und mit FPGA sowie ASIC-Toolchains kompatibel ist.  

Das Hauptziel von SpinalHDL ist es, die Entwicklung digitaler Schaltung einfacher, produktiver und vor allem zuverlässiger zu machen.  
Im Gegensatz zu alten, traditionellen HDLs wie VHDL oder Verilog, die fehleranfällig und schwerfällig sind, bietet SpinalHDL eine moderne Syntax.  
Damit können Entwickler Schaltungen klar, modular und wiederverwendbar beschreiben.
Durch die Integration bewährter Prinzipien aus der Softwareentwicklung wie Unit Tests, parametrisierbare Module und IDE Unterstützung entsteht ein Workflow, 
der sowohl präzise als auch effizient ist.  
Gleichzeitig bleibt SpinalHDL voll kompatibel mit FPGA und ASIC Toolchains, da automatisch Verilog oder VHDL Code generiert wird.


## Überblick über traditionelle HDLs (VHDL/Verilog)
Um die Vorteile von SpinalHDL besser einordnen zu können, lohnt sich ein Blick auf die 
traditionellen Hardwarebeschreibungssprachen VHDL und Verilog. Beide wurden in den 
1980er-Jahren entwickelt und haben sich als Industriestandard etabliert. Trotz ihrer 
Verbreitung bringen sie jedoch erhebliche Nachteile mit sich.

- **Geringe Abstraktion:** Strukturelle Wiederverwendung und Parametrisierung sind schwierig.  
- **Schlechte Fehlerdiagnose:** Kompilierungsfehler liefern oft kryptische Fehlermeldungen.  
- **Statischer Code-Struktur:** Keine Möglichkeit zur dynamischen Erzeugung von Komponenten.
- **Mangelnde Integration moderner Softwarepraktiken:** Unit-Tests, modulare Softwaremuster 
  oder IDE-Integration sind nur eingeschränkt möglich.
Diese Einschränkungen machen klassische HDLs gerade bei komplexen Projekten schwer 
handhabbar und mindern sowohl die Produktivität als auch die Wartbarkeit. Genau an 
dieser Stelle setzt SpinalHDL an.

## Warum die Abkehr sinnvoll ist
Moderne Hardwareentwicklungsprojekte profitieren zunehmend von Prinzipien der 
Softwareentwicklung. Dazu gehören die Wiederverwendbarkeit durch modulare Bausteine, 
die Testbarkeit durch Simulation und automatisierte Prüfungen sowie die Abstraktion durch 
objektorientierte oder funktionale Programmierung. SpinalHDL vereint diese Stärken und 
ermöglicht gleichzeitig die Generierung von synthetisierbarem Verilog- oder VHDL-Code, 
der problemlos in bestehende Toolchains integriert werden kann. 

#  Grundlagen von SpinalHDL

SpinalHDL ist eine Hardwarebeschreibungssprache, die als **Domain Specific Language (DSL)** in **Scala** implementiert ist. Sie bietet gegenüber VHDL und Verilog eine moderne, typensichere und modulare Beschreibung von Schaltungen.

## Variablendeklaration in SpinalHDL

Die wichtigsten Typen zur Signalbeschreibung:

| Typ    | Beschreibung                   | Beispiel                     |
|--------|--------------------------------|------------------------------|
| `Bool` | Ein einzelnes Bit (true/false) | `val myBit = Bool()`         |
| `UInt` | Unsigned Integer (z. B. 8 Bit) | `val count = UInt(8 bits)`   |
| `SInt` | Signed Integer                 | `val x = SInt(16 bits)`      |
| `Bits` | Bit-Vektor ohne Interpretation | `val raw = Bits(4 bits)`     |

> In SpinalHDL beschreibt `val` eine **konstante Referenz auf ein Signalobjekt** – nicht das Signal selbst wie in Verilog.
## Signale vs. Register

```scala
val a = UInt(8 bits)       // Kombinatorisch (wire)
val b = Reg(UInt(8 bits))  // Getaktetes Register
```

- `Reg(...)` erzeugt ein Flip-Flop (Register) mit Initialwert:  

```scala
val count = Reg(UInt(4 bits)) init(0)
```

## Steuerstrukturen

Wie in Scala aber spezialisiert für Hardwarelogik:

~~~scala
when(cond) {
  // true-Zweig
} elsewhen(otherCond) {
  // anderer Zweig
} otherwise {
  // fallback-Zweig
}
~~~

Beispiel:

```scala
val out = Bool()
when(io.a === io.b) {
  out := True
} otherwise {
  out := False
}
```

## Bundles (Schnittstellen)

Ein `Bundle` ist wie ein `struct`:

```scala
val io = new Bundle {
  val start = in Bool()
  val done  = out Bool()
  val value = in UInt(8 bits)
}
```
 Alle Signale im Bundle sind typisiert (`in`, `out`, `inout`).

## Vektoren und Arrays

```scala
val vec = Vec(UInt(8 bits), 4)
val arr = Array.fill(4)(UInt(8 bits))
```
Vektoren erlauben z. B. Busse, Speicher, Registergruppen.

## Komponentenstruktur

Eine Hardwareeinheit (Modul) ist eine Klasse, die von `Component` erbt:

```scala
class MyModule extends Component {
  val io = new Bundle {
    val a = in UInt(8 bits)
    val b = in UInt(8 bits)
    val result = out UInt(8 bits)
  }

  io.result := io.a + io.b
}
```

## Top-Level mit Verilog-Ausgabe

```scala
object MyModuleVerilog {
  def main(args: Array[String]): Unit = {
    SpinalVerilog(new MyModule)
  }
}
```

## Typisches Verhalten vs. VHDL

| Aktion                | VHDL                  | SpinalHDL                         |
|-----------------------|-----------------------|-----------------------------------|
| Signal zuweisen       | `a <= b;`             | `a := b`                          |
| Wenn-Bedingung        | `if...elsif...else`   | `when...elsewhen...otherwise`    |
| Register mit Reset    | Prozess mit Reset     | `Reg(...) init(...)`              |
| Strukturierte I/Os    | Record / Port Map     | `Bundle`, `in/out`                |

## Besonderheiten

- **stark typisiert** – viele Fehler werden vom Compiler erkannt  
- **parametrisierbar** – Bausteine können generisch sein  
- **simulationsfähig** – direkt in Scala testbar  
- **Verilog/VHDL-Ausgabe** – leicht integrierbar  

## TL;DR für Anfänger

| Du willst …         | … dann nutze             |
|---------------------|--------------------------|
| 1 Bit Signal        | `Bool()`                 |
| 8 Bit Zähler        | `Reg(UInt(8 bits))`      |
| Multiplexer         | `Mux(sel, a, b)`         |
| Verzweigung         | `when { ... }`           |
| Interface           | `new Bundle { ... }`     |

#  Struktur und Aufbau eines SpinalHDL-Projekts

## Ordnerstruktur
Ein SpinalHDL-Projekt orientiert sich in der Regel an der typischen Struktur von Scala-Projekten. 
Die Dateien sind so gegliedert, dass eine klare Trennung zwischen Entwurf, Test und generiertem 
Code besteht. Ein mögliches Projekt kann beispielsweise folgendermaßen aufgebaut sein:
```text
my-spinal-project/
├── build.sbt
├── src/
│   ├── main/
│   │   └── scala/           // SpinalHDL-Komponenten
│   └── test/
│       └── scala/           // Simulation und Unit-Tests
├── generated/               // generierter Verilog/VHDL
└── README.md
```

## Entwicklungsumgebung
Für die Arbeit mit SpinalHDL empfiehlt sich die Verwendung einer modernen Entwicklungsumgebung.  
In der Praxis hat sich **IntelliJ IDEA** mit installiertem Scala-Plugin bewährt. Damit stehen Funktionen wie Code-Vervollständigung, Syntaxhervorhebung und Refactoring zur Verfügung, die die Entwicklung deutlich vereinfachen. Als basis werden **Java JDK (Java 17)**, **Scala 2.13** sowie **sbt (Scala Build Tool)** benötigt
Als Build-Tool wird **sbt (Scala Build Tool)** eingesetzt. **sbt** verwaltet die Abhängigkeiten, kompiliert den Quellcode und führt Programme aus. Dadurch lässt sich der gesamte Entwicklungsprozess strukturiert und reproduzierbar abwickeln.

Zur Simulation kommen häufig **Verilator** oder **GHDL** zum Einsatz. Diese Werkzeuge ermöglichen eine schnelle und präzise Verifikation des Verhaltens der entworfenen Schaltungen und sind in der Community weit verbreitet.


## Beispiel-Kommando
Die folgenden Befehle zeigen einen typischen Ablauf beim Arbeiten mit einem SpinalHDL-Projekt:
```bash
sbt compile
sbt run
```


#  Vorteile von SpinalHDL gegenüber traditionellen HDLs

## Syntax und Typsicherheit
SpinalHDL basiert auf Scala und profitiert von einer modernen, stark typisierten Syntax. Typfehler oder fehlerhafte Verbindungen zwischen Signalen werden bereits während der Kompilierung erkannt. Dadurch lassen sich viele Probleme ausschließen, die in klassischen HDLs oft erst bei der Simulation oder sogar im Syntheseprozess sichtbar werden.

## Abstraktion und Wiederverwendbarkeit
Durch Vererbung, generische Klassen und parametrisierte Module können Komponenten einfach angepasst und wiederverwendet werden. Entwicklerinnen und Entwickler können Schleifen, Funktionen oder Bedingungen einsetzen und sogar Fabriken für Komponenten erstellen. Damit wird eine hohe Flexibilität erreicht, die klassische HDLs in dieser Form nicht bieten.

## Fehlerdiagnose
Fehlermeldungen in SpinalHDL enthalten vollständige Stacktraces aus Scala und zeigen präzise auf die Quelle eines Problems. Wenn beispielsweise eine ungültige Zuweisung oder ein mehrfach getriebenes Signal vorliegt, wird dies direkt sichtbar. Dadurch wird die Fehlersuche erheblich vereinfacht und Entwicklungszeit eingespart.

## Simulation & Debugging
Da SpinalHDL in Scala integriert ist, können Schaltungen direkt in **IntelliJ IDEA** simuliert werden. Mit Hilfsmitteln wie `SimConfig` und `ScalaTest` lassen sich präzise und wiederholbare Testfälle erstellen. Dies ermöglicht eine enge Verzahnung von Entwicklung, Simulation und Verifikation und erleichtert das Debugging erheblich.

#  Entwicklungsworkflow

In SpinalHDL folgt ein typischer Designprozess drei Phasen:

1. **Komponentenbeschreibung** (Design)
2. **Simulation & Verifikation** (Test)
3. **Codegenerierung** (Export in Verilog/VHDL)

##   Komponentenbeschreibung

Hier wird das gewünschte Verhalten in einem Modul (Component) beschrieben.

```scala
class Adder extends Component {
  val io = new Bundle {
    val a, b = in UInt(8 bits)
    val result = out UInt(8 bits)
  }
  io.result := io.a + io.b
}
```
###  Erklärung :

- `class Adder extends Component`: definiert eine neue SpinalHDL-Komponente.
- `val io = new Bundle { ... }`: legt die I/O-Schnittstelle fest.
  - `a`, `b`: 8-Bit Eingänge (z. B. zwei Summanden)
  - `result`: 8-Bit Ausgang (Summe)
- `io.result := io.a + io.b`: beschreibt die Logik: Addition von `a` und `b`, das Ergebnis wird ausgegeben.

**Das ist reine Kombinatorik**, kein Register (d.h. keine Speicherung, kein Takt).

##   Simulationsmöglichkeiten

Mit SpinalHDL kannst du direkt in Scala simulieren.

```scala
SimConfig.withWave.compile(new Adder).doSim { dut =>
  dut.io.a #= 4
  dut.io.b #= 7
  dut.clockDomain.forkStimulus(10)
  dut.clockDomain.waitSampling()
  assert(dut.io.result.toInt == 11)
}
```
###  Erklärung :

- `SimConfig.withWave`: Aktiviert Wellenform-Ausgabe (`.vcd`).
- `compile(new Adder)`: kompiliert die Adder-Komponente für Simulation.
- `doSim { dut => ... }`: definiert, was im Simulationslauf passieren soll.

**Innerhalb des Blocks:**
- `dut.io.a #= 4`: Setzt Eingang `a` auf 4
- `dut.io.b #= 7`: Setzt Eingang `b` auf 7
- `forkStimulus(10)`: Erzeugt Taktsignal mit Periodendauer 10
- `waitSampling()`: Wartet auf eine steigende Taktflanke
- `assert(...)`: Prüft, ob das Ergebnis tatsächlich 11 ist

>  Hinweis: Die Simulation verwendet dieselbe Logik wie der Synthese-Code, sie ist somit **cycle-accurate**.

## Code generieren (Verilog/VHDL)

Mit einem einfachen Aufruf generierst du RTL-Code:

```scala
SpinalVerilog(new Adder)
SpinalVhdl(new Adder)
```
- `SpinalVerilog(...)`: erzeugt eine `.v`-Datei (Verilog)
- `SpinalVhdl(...)`: erzeugt eine `.vhd`-Datei (VHDL)
- Die Datei enthält exakt das, was von Tools wie **Vivado**, **Quartus**, **Yosys**, etc. verarbeitet werden kann

 Der generierte Code wird im aktuellen Arbeitsverzeichnis gespeichert oft in einem Unterordner wie `./rtl/` oder `./simWorkspace/Adder`.


##  Zusammengefasst:

| Schritt          | Ziel                           | Beispiel                          |
|------------------|--------------------------------|-----------------------------------|
| Komponentenbau   | Schaltung entwerfen            | `new Adder`                       |
| Simulation       | Verhalten testen               | `doSim { ... }`                   |
| Codegenerierung  | Verilog/VHDL für Synthesis     | `SpinalVerilog(...)


#  Praxisbeispiele
Im Folgenden werden einige typische Praxisbeispiele vorgestellt, die den Einsatz von SpinalHDL verdeutlichen. Jedes Beispiel enthält die Beschreibung des Moduls, eine Testbench zur Simulation sowie die Möglichkeit, eine Verilog-Datei zu generieren. Auf diese Weise wird der komplette Ablauf von der Modellierung über die Verifikation bis zur Codegenerierung sichtbar.

## Comparator

Ein Comparator vergleicht zwei Werte (`a` und `b`) und erzeugt Ausgänge für:
- Gleichheit (`equal`)
- Größer-als (`greater`)
- Kleiner-als (`less`)
  
**Projektstruktur**
```
comparator-spinalhdl/
├── build.sbt
├── src/
│   ├── main/scala/
│   │   ├── Comparator.scala        // Comparator-Modul
│   │   └── ComparatorVerilog.scala // Verilog-Generierung
│   │   └── ComparatorVhdl.scala    // VHDL-Generierung
│   └── test/scala/
│       └── ComparatorSim.scala     // Testbench
└── README.md
```

**Aufbau des Moduls**

```scala
import spinal.core._

class Comparator(width: Int) extends Component {
  noIoPrefix()
  setDefinitionName("Comparator")

  val io = new Bundle {
    val a       = in  UInt(width bits)
    val b       = in  UInt(width bits)
    val equal   = out Bool()
    val greater = out Bool()
    val less    = out Bool()
  }

  io.a.setName("a")
  io.b.setName("b")
  io.equal   := io.a === io.b
  io.greater := io.a > io.b
  io.less    := io.a < io.b

  io.equal.setName("eq")
  io.greater.setName("gt")
  io.less.setName("lt")
}
```
**Was macht das Modul?**

- Es nimmt zwei `UInt`-Eingänge `a` und `b`.
- Es vergleicht sie in Echtzeit.
- Setzt genau ein Ergebnis-Signal auf `true`:
  - `equal`: wenn `a == b`
  - `greater`: wenn `a > b`
  - `less`: wenn `a < b`

**Testbench: `ComparatorSim.scala`**
```scala
import spinal.core._
import spinal.core.sim._

object ComparatorSim {
  def main(args: Array[String]): Unit = {
    SimConfig
      .withVcdWave
      .compile(new Comparator(4))
      .doSim { dut =>
        dut.io.a #= 5
        dut.io.b #= 5
        sleep(1)
        assert(dut.io.equal.toBoolean)

        dut.io.a #= 7
        dut.io.b #= 4
        sleep(1)
        assert(dut.io.greater.toBoolean)

        dut.io.a #= 2
        dut.io.b #= 8
        sleep(1)
        assert(dut.io.less.toBoolean)

        simSuccess()
      }
  }
}
```


**Verilog-Ausgabe: `ComparatorVerilog.scala`**
```scala
import spinal.core._

object ComparatorVerilog {
  def main(args: Array[String]): Unit = {
    SpinalConfig(
      targetDirectory = "generated/verilog",
      oneFilePerComponent = true
    ).generateVerilog(new Comparator(4).setDefinitionName("Comparator"))
  }
}
```

**VHDL-Ausgabe: `ComparatorVhdl.scala`**
```scala
import spinal.core._

object ComparatorVhdl {
  def main(args: Array[String]): Unit = {
    SpinalConfig(
      targetDirectory = "generated/vhdl",
      oneFilePerComponent = true
    ).generateVhdl(new Comparator(4).setDefinitionName("Comparator"))
  }
}
```

**Verwendung**
```bash
sbt compile
sbt "runMain ComparatorSim"
sbt "runMain ComparatorVerilog"
sbt "runMain ComparatorVhdl"
```

Ergebnis: Die Dateien `Comparator.v` und `Comparator.vhd` werden generiert, und die Testbench prüft die Vergleichsfunktionen.

**Generierter VHDL-Code: `Comparator.vhd`** 
```scala
-- Generator : SpinalHDL v1.9.1    git head : 9cba1927b2fff87b0d54e8bbecec94e7256520e4
-- Component : Comparator

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library work;
use work.pkg_scala2hdl.all;
use work.all;
use work.pkg_enum.all;


entity Comparator is
  port(
    a : in unsigned(3 downto 0);
    b : in unsigned(3 downto 0);
    eq : out std_logic;
    gt : out std_logic;
    lt : out std_logic
  );
end Comparator;

architecture arch of Comparator is

begin
  eq <= pkg_toStdLogic(a = b);
  gt <= pkg_toStdLogic(b < a);
  lt <= pkg_toStdLogic(a < b);
end arch;
```
**Generierter Verilog-Code: `Comparator.v`** 
```verilog
// Generator : SpinalHDL v1.9.1    git head : 9cba1927b2fff87b0d54e8bbecec94e7256520e4
// Component : Comparator

`timescale 1ns/1ps 
module Comparator (
  input      [3:0]    a,
  input      [3:0]    b,
  output              eq,
  output              gt,
  output              lt
);


  assign eq = (a == b);
  assign gt = (b < a);
  assign lt = (a < b);

endmodule
```

## Zähler

Ein Zähler zählt bei jedem Takt um 1 nach oben. Er kann in vielen Anwendungen eingesetzt werden, z. B. als Zeitgeber, Schleifenzähler oder zur Adressierung.

**Projektstruktur**
```
counter-spinalhdl/
├── build.sbt
├── src/
│   ├── main/scala/
│   │   ├── Counter.scala        // Zähler-Modul
│   │   └── CounterVerilog.scala // Verilog-Generierung
│   │   └── CounterVhdl.scala    // VHDL-Generierung
│   └── test/scala/
│       └── CounterSim.scala     // Testbench
└── README.md
```

**Aufbau des Moduls**

```scala
import spinal.core._

class Counter(width: Int) extends Component {
  noIoPrefix()
  setDefinitionName("Counter")

  val io = new Bundle {
    val enable = in Bool()
    val reset  = in Bool()
    val value  = out UInt(width bits)
  }

  val count = Reg(UInt(width bits)) init(0)
  when(io.reset) { count := 0 } .elsewhen(io.enable) { count := count + 1 }
  io.value := count

  io.enable.setName("enable"); io.reset.setName("reset"); io.value.setName("value")
}
```
**Was macht das Modul?**

- `enable`: Wenn aktiv, zählt der Zähler hoch.
- `reset`: Wenn aktiv, wird der Zähler auf 0 gesetzt.
- `value`: Der aktuelle Zählerwert.

**Testbench: `CounterSim.scala`**

```scala
import spinal.core._
import spinal.sim._
import spinal.core.sim._

object CounterSim {
  def main(args: Array[String]): Unit = {
    SimConfig
      .withVcdWave                // VCD für GTKWave
      .compile(new Counter(4))
      .doSim { dut =>
        dut.clockDomain.forkStimulus(10)

        dut.io.reset  #= true
        dut.io.enable #= false
        dut.clockDomain.waitSampling()

        dut.io.reset  #= false
        dut.io.enable #= true

        for (_ <- 0 until 8) {
          dut.clockDomain.waitSampling()
          println(s"Zählerwert = ${dut.io.value.toBigInt}")
        }

        simSuccess()
      }
  }
}
```

**Verilog-Ausgabe: `CounterVerilog.scala`**

```scala
import spinal.core._

object CounterVerilog {
  def main(args: Array[String]): Unit =
    SpinalConfig(targetDirectory="generated/verilog", oneFilePerComponent=true)
      .generateVerilog(new Counter(4).setDefinitionName("Counter"))
}
```

**VHDL-Ausgabe: `CounterVhdl.scala`**

```scala
import spinal.core._
object CounterVhdl {
  def main(args: Array[String]): Unit =
    SpinalConfig(targetDirectory="generated/vhdl", oneFilePerComponent=true)
      .generateVhdl(new Counter(4).setDefinitionName("Counter"))
}
```
**Verwendung**

```bash
sbt compile
sbt "runMain CounterSim"
sbt "runMain CounterVerilog"
```

**Ergebnis:**
Die Dateien `Counter.v` und `Counter.vhd` werden generiert. In der Simulation zählt der Wert bei `enable = true` hoch.

**Generierter VHDL-Code: `Counter.vhd`** 
```scala
-- Generator : SpinalHDL v1.9.1    git head : 9cba1927b2fff87b0d54e8bbecec94e7256520e4
-- Component : Counter

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library work;
use work.pkg_scala2hdl.all;
use work.all;
use work.pkg_enum.all;


entity Counter is
  port(
    enable : in std_logic;
    reset : in std_logic;
    value : out unsigned(3 downto 0);
    clk : in std_logic;
    reset_1 : in std_logic
  );
end Counter;

architecture arch of Counter is

  signal zz_value : unsigned(3 downto 0);
begin
  value <= zz_value;
  process(clk, reset_1)
  begin
    if reset_1 = '1' then
      zz_value <= pkg_unsigned("0000");
    elsif rising_edge(clk) then
      if reset = '1' then
        zz_value <= pkg_unsigned("0000");
      else
        if enable = '1' then
          zz_value <= (zz_value + pkg_unsigned("0001"));
        end if;
      end if;
    end if;
  end process;

end arch;
```
**Generierter Verilog-Code: `Counter.v`** 
```verilog
// Generator : SpinalHDL v1.9.1    git head : 9cba1927b2fff87b0d54e8bbecec94e7256520e4
// Component : Counter

`timescale 1ns/1ps 
module Counter (
  input               enable,
  input               reset,
  output     [3:0]    value,
  input               clk,
  input               reset_1
);

  reg        [3:0]    _zz_value;

  assign value = _zz_value;
  always @(posedge clk or posedge reset_1) begin
    if(reset_1) begin
      _zz_value <= 4'b0000;
    end else begin
      if(reset) begin
        _zz_value <= 4'b0000;
      end else begin
        if(enable) begin
          _zz_value <= (_zz_value + 4'b0001);
        end
      end
    end
  end


endmodule
```

## Taktteiler (Clock Divider)

Ein Taktteiler erzeugt aus einem schnellen Eingangstakt einen langsameren Ausgangstakt, indem er Takte zählt und z. B. nur jedes 256. Signal durchlässt.

**Projektstruktur**
```
clockdivider-spinalhdl/
├── build.sbt
├── src/
│   ├── main/scala/
│   │   ├── ClockDivider.scala        // Taktteiler-Modul
│   │   └── ClockDividerVerilog.scala // Verilog-Generierung
│   │   └── ClockDividerVhdl.scala    // VHDL-Generierung
│   └── test/scala/
│       └── ClockDividerSim.scala     // Testbench
└── README.md
```

**Aufbau des Moduls**

```scala
import spinal.core._

class ClockDivider(divisorWidth: Int) extends Component {
  noIoPrefix()
  setDefinitionName("ClockDivider")

  val io = new Bundle {
    val clkOut = out Bool()
     val counterO = out UInt(divisorWidth bits)   //  internal counter
  }

  // Zähler läuft kontinuierlich
  val counter = Reg(UInt(divisorWidth bits)) init(0)
  counter := counter + 1

  // höchstwertiges Bit als geteiltes Taktsignal
  io.clkOut := counter.msb
  io.counterO := counter

  io.clkOut.setName("clkOut")
  io.counterO.setName("counter")
}
```
**Was macht das Modul?**

- `counter`: Zählt kontinuierlich bei jedem Takt.
- `msb`: Der höchste Bitwert des Zählers (Most Significant Bit) wird als geteilter Takt ausgegeben.
- **Beispiel**: Bei `divisorWidth = 8` ergibt sich ein Teiler von 256 (halbe Periode = 128 Takte).


**Testbench: `ClockDividerSim.scala`**
```scala
import spinal.core._
import spinal.core.sim._

object ClockDividerSim {
  def main(args: Array[String]): Unit = {
    SimConfig.withVcdWave.compile(new ClockDivider(8)).doSim { dut =>
      dut.clockDomain.forkStimulus(10)

      for (i <- 0 until 300) {
        dut.clockDomain.waitSampling()
        if (i % 50 == 0)
          println(s"Takt $i: clkOut = ${dut.io.clkOut.toBoolean}")
      }

      simSuccess()
    }
  }
}
```
**Verilog-Ausgabe: `ClockDividerVerilog.scala`**

```scala
import spinal.core._

object ClockDividerVerilog {
  def main(args: Array[String]): Unit = {
    SpinalConfig(
      targetDirectory = "generated/verilog",
      oneFilePerComponent = true
    ).generateVerilog(new ClockDivider(8).setDefinitionName("ClockDivider"))
  }
}
```

**VHDL-Ausgabe: `ClockDividerVhdl.scala`**
```scala
import spinal.core._

object ClockDividerVhdl {
  def main(args: Array[String]): Unit = {
    SpinalConfig(
      targetDirectory = "generated/vhdl",
      oneFilePerComponent = true
    ).generateVhdl(new ClockDivider(8).setDefinitionName("ClockDivider"))
  }
}
```

**Verwendung**
```bash
sbt compile
sbt "runMain ClockDividerSim"
sbt "runMain ClockDividerVerilog"
sbt "runMain ClockDividerVhdl"
```

Das erzeugt:
- `ClockDivider.v`: die Verilog-Datei
- `ClockDivider.vhd`: die Verilog-Datei
- und zeigt die Simulation mit `clkOut`, der etwa alle 128 Takte wechselt.

**Generierter VHDL-Code: `ClockDivider.vhd`** 
```scala
-- Generator : SpinalHDL v1.9.1    git head : 9cba1927b2fff87b0d54e8bbecec94e7256520e4
-- Component : ClockDivider

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library work;
use work.pkg_scala2hdl.all;
use work.all;
use work.pkg_enum.all;


entity ClockDivider is
  port(
    clkOut : out std_logic;
    clk : in std_logic;
    reset : in std_logic
  );
end ClockDivider;

architecture arch of ClockDivider is

  signal zz_clkOut : unsigned(7 downto 0);
begin
  clkOut <= pkg_extract(zz_clkOut,7);
  process(clk, reset)
  begin
    if reset = '1' then
      zz_clkOut <= pkg_unsigned("00000000");
    elsif rising_edge(clk) then
      zz_clkOut <= (zz_clkOut + pkg_unsigned("00000001"));
    end if;
  end process;

end arch;
```

**Generierter Verilog-Code: `ClockDivider.v`** 
```verilog
// Generator : SpinalHDL v1.9.1    git head : 9cba1927b2fff87b0d54e8bbecec94e7256520e4
// Component : ClockDivider

`timescale 1ns/1ps 
module ClockDivider (
  output              clkOut,
  input               clk,
  input               reset
);

  reg        [7:0]    _zz_clkOut;

  assign clkOut = _zz_clkOut[7];
  always @(posedge clk or posedge reset) begin
    if(reset) begin
      _zz_clkOut <= 8'h00;
    end else begin
      _zz_clkOut <= (_zz_clkOut + 8'h01);
    end
  end


endmodule
```

## PWM

Dies ist ein einfaches SpinalHDL-Projekt, das ein parametrierbares PWM-Modul (Pulsweitenmodulation) implementiert. Es enthält:

- eine Hardwarebeschreibung (`Pwm.scala`)
- eine Testbench (`PwmSim.scala`)
- eine Verilog-Ausgabe (`PwmVerilog.scala`)
- eine VHDL-Ausgabe (`PwmVhdl.scala`)
- die Hilfsskripte `scripts/sim.sh` (Simulation) und `scripts/gen.sh` (HDL-Generierung)
- und eine verständliche Erklärung des Funktionsprinzips

**Projektstruktur**

```
pwm-spinalhdl/
├── build.sbt
├── project/
│   └── build.properties
├── src/
│   ├── main/
│   │   └── scala/
│   │       ├── Pwm.scala                 ← [1] PWM-Modul
│   │       └── PwmVerilog.scala          ← [3] Verilog-Generierung
│   │       └── PwmVhdl.scala             ← [4] VHDL-Generierung
│   └── test/
│       └── scala/
│           └── PwmSim.scala              ← [2] Simulation
├── scripts/
│   ├── sim.sh                            ←  Simulation
│   └── gen.sh                            ←  HDL-Generierung
└── generated/
│   ├── verilog/
│       └── Pwm.v
│   └── vhdl/
│       └── Pwm.vhd
```

**Erklärung des PWM-Moduls**

Das PWM-Modul erzeugt ein Signal, das schnell zwischen **an (1)** und **aus (0)** wechselt.  
Wie lange das Signal „an“ bleibt, hängt vom **Duty-Cycle** ab – einem Eingabewert, der angibt, wie viel Prozent der Zeit das Signal „an“ sein soll.

**Aufbau des Moduls**

```scala
import spinal.core._

class Pwm(width: Int) extends Component {
  noIoPrefix()
  setDefinitionName("Pwm")

  val io = new Bundle {
    val enable  = in  Bool()
    val duty    = in  UInt(width bits)   // 0 .. 2^width-1
    val pwmOut  = out Bool()
    val dutyPct = out UInt(7 bits)       // <-- OUTPUT as percentage
  }

  val counter = Reg(UInt(width bits)) init(0)
  counter := counter + 1
  io.pwmOut := io.enable && (counter < io.duty)

  
  val numWidth = width + 7
  val num      = io.duty.resize(numWidth) * U(100)
  val den      = U((1 << width) - 1, numWidth bits)
  val pctWide  = (num + (den >> 1)) / den
  io.dutyPct   := pctWide.resized          

  
  io.enable.setName("enable")
  io.duty.setName("duty")
  io.pwmOut.setName("pwmOut")
  io.dutyPct.setName("dutyPct")
}
```

**Was macht das Modul?**

- `width`: Gibt an, wie genau das PWM-Signal sein soll (z. B. 8 Bit → Werte von 0 bis 255).
- `enable`: Schaltet das PWM-Signal ein oder aus.
- `duty`: Bestimmt, wie lange das Signal „an“ sein soll (je höher der Wert, desto länger).
- `counter`: Zählt von 0 bis zum Maximalwert und beginnt dann wieder von vorn.
- `pwmOut`: Wird „an“, solange `counter < duty`.
- `dutyPct`: Zeigt den Duty-Cycle direkt in Prozent (20%, 50%, 75%, 0% oder 100%)

###  Beispiel (bei 8 Bit Auflösung)

- `duty = 0` → Signal ist immer aus → 0%
- `duty = 128` → Signal ist 50 % der Zeit an
- `duty = 255` → Signal ist immer an → 100%

Das Modul vergleicht einen Zähler mit einem Zielwert (`duty`).  
Solange der Zähler kleiner ist, ist das Signal **an**  danach **aus**.  
Dieser Zyklus wiederholt sich kontinuierlich.

**[1] `src/main/scala/Pwm.scala` (Code wie oben)**

Siehe oben unter „Aufbau des Moduls“.

**[2] `src/test/scala/PwmSim.scala`**

```scala
import spinal.core._
import spinal.core.sim._

object PwmSim {
  def main(args: Array[String]): Unit = {
    SimConfig.withVcdWave.compile(new Pwm(8)).doSim { dut =>
      dut.clockDomain.forkStimulus(10)

      // enable PWM
      dut.io.enable #= true

      // 25% duty
      dut.io.duty #= 64
      for (_ <- 0 until 300) dut.clockDomain.waitSampling()

      // 50% duty
      dut.io.duty #= 128
      for (_ <- 0 until 300) dut.clockDomain.waitSampling()

      // 75% duty
      dut.io.duty #= 192
      for (_ <- 0 until 300) dut.clockDomain.waitSampling()

      // 0% duty
      dut.io.duty #= 0
      for (_ <- 0 until 150) dut.clockDomain.waitSampling()

      // 100% duty
      dut.io.duty #= 255
      for (_ <- 0 until 150) dut.clockDomain.waitSampling()

      simSuccess()
    }
  }
}
```

**`[3]PwmVerilog.scala`**
```scala
import spinal.core._
object PwmVerilog {
  def main(args: Array[String]): Unit =
    SpinalConfig(targetDirectory="generated/verilog", oneFilePerComponent=true)
      .generateVerilog(new Pwm(8).setDefinitionName("Pwm"))
}
```

**`[4]PwmVhdl.scala`**
```scala
import spinal.core._
object PwmVhdl {
  def main(args: Array[String]): Unit =
    SpinalConfig(targetDirectory="generated/vhdl", oneFilePerComponent=true)
      .generateVhdl(new Pwm(8).setDefinitionName("Pwm"))
}
```

**`sim.sh`**
```scala
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
docker run --rm -it \
  -u $(id -u):$(id -g) -e HOME=/tmp \
  -v "$PWD":/workspace -w /workspace \
  spinalhdl:dev \
  sbt "Test / runMain PwmSim"
echo "✅ PWM: VCD under simWorkspace/Pwm/"
```

**`gen.sh`**
```scala
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
docker run --rm -it \
  -u $(id -u):$(id -g) -e HOME=/tmp \
  -v "$PWD":/workspace -w /workspace \
  spinalhdl:dev \
  sbt "runMain PwmVerilog" "runMain PwmVhdl"
echo "✅ PWM: HDL under generated/{verilog,vhdl}/"
```


**Projekt kompilieren und starten**
```bash
./scripts/sim.sh  #Simulation mit VCD
```
```bash
./scripts/gen.sh  #HDL-Ausgabe (Verilog und VHDL)
```

**Generierter Verilog-Code: `Pwm.v`** 
```verilog
// Generator : SpinalHDL v1.9.1    git head : 9cba1927b2fff87b0d54e8bbecec94e7256520e4
// Component : Pwm

`timescale 1ns/1ps 
module Pwm (
  input               enable,
  input      [7:0]    duty,
  output              pwmOut,
  output     [6:0]    dutyPct,
  input               clk,
  input               reset
);

  wire       [21:0]   _zz_dutyPct_1;
  wire       [21:0]   _zz_dutyPct_2;
  wire       [21:0]   _zz_dutyPct_3;
  wire       [14:0]   _zz_dutyPct_4;
  wire       [21:0]   _zz_dutyPct_5;
  wire       [13:0]   _zz_dutyPct_6;
  reg        [7:0]    _zz_pwmOut;
  wire       [14:0]   _zz_dutyPct;

  assign _zz_dutyPct_1 = (_zz_dutyPct_2 / _zz_dutyPct);
  assign _zz_dutyPct_2 = (_zz_dutyPct_3 + _zz_dutyPct_5);
  assign _zz_dutyPct_3 = (_zz_dutyPct_4 * 7'h64);
  assign _zz_dutyPct_4 = {7'd0, duty};
  assign _zz_dutyPct_6 = (_zz_dutyPct >>> 1'd1);
  assign _zz_dutyPct_5 = {8'd0, _zz_dutyPct_6};
  assign pwmOut = (enable && (_zz_pwmOut < duty));
  assign _zz_dutyPct = 15'h00ff;
  assign dutyPct = _zz_dutyPct_1[6:0];
  always @(posedge clk or posedge reset) begin
    if(reset) begin
      _zz_pwmOut <= 8'h00;
    end else begin
      _zz_pwmOut <= (_zz_pwmOut + 8'h01);
    end
  end


endmodule
```

**Generierter VHDL-Code: `Pwm.vhd`** 
```scala
-- Generator : SpinalHDL v1.9.1    git head : 9cba1927b2fff87b0d54e8bbecec94e7256520e4
-- Component : Pwm

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library work;
use work.pkg_scala2hdl.all;
use work.all;
use work.pkg_enum.all;


entity Pwm is
  port(
    enable : in std_logic;
    duty : in unsigned(7 downto 0);
    pwmOut : out std_logic;
    dutyPct : out unsigned(6 downto 0);
    clk : in std_logic;
    reset : in std_logic
  );
end Pwm;

architecture arch of Pwm is

  signal zz_pwmOut : unsigned(7 downto 0);
  signal zz_dutyPct : unsigned(14 downto 0);
begin
  pwmOut <= (enable and pkg_toStdLogic(zz_pwmOut < duty));
  zz_dutyPct <= pkg_unsigned("000000011111111");
  dutyPct <= pkg_resize((((pkg_resize(duty,15) * pkg_unsigned("1100100")) + pkg_resize(pkg_shiftRight(zz_dutyPct,1),22)) / zz_dutyPct),7);
  process(clk, reset)
  begin
    if reset = '1' then
      zz_pwmOut <= pkg_unsigned("00000000");
    elsif rising_edge(clk) then
      zz_pwmOut <= (zz_pwmOut + pkg_unsigned("00000001"));
    end if;
  end process;

end arch;
```

**Ergebnis**

- Wir erhalten ein synthetisierbares PWM-Modul  
- Wir können das Verhalten direkt simulieren  
- Die generierte Verilog-Code (`Pwm.v`) und VHDL-Code (`Pwm.vhd`) sind für FPGA/ASIC verwendbar

# Komplexere Designs: Der VexRiscv-Prozessor
SpinalHDL eignet sich nicht nur für kleine Module wie Zähler oder PWM-Generatoren. 
Es kann auch für sehr große und komplexe Designs verwendet werden. Ein bekanntes Beispiel dafür ist der **VexRiscv-Prozessor**.  

Der VexRiscv ist ein vollständiger 32-Bit-RISC-V-Prozessor, der vollständig in SpinalHDL 
geschrieben wurde. Er wird in vielen FPGA-Projekten eingesetzt und ist in der 
Open-Source-Community weit verbreitet.  

## Architektur
Der Prozessor basiert auf einer **Pipeline-Architektur**. Das bedeutet, dass die 
Abarbeitung von Instruktionen in mehrere Schritte aufgeteilt wird, die parallel 
ausgeführt werden können.  

Ein einfaches Bild dafür ist eine Fabrikstraße: während ein Arbeitsschritt an einer 
Instruktion gerade ausgeführt wird, befindet sich die nächste Instruktion bereits 
in der folgenden Station. Dadurch wird die Ausführung schneller und effizienter.  

**Pipeline-Skizze:**

![Pipeline sketch](https://github.com/user-attachments/assets/91404905-f756-4b6a-950c-4e9791b61e3d)
Die Abbildung zeigt eine 5-Stufen-Pipeline, in der mehrere Instruktionen überlappend 
bearbeitet werden.  

- **IF (Instruction Fetch):** Instruktion wird aus dem Speicher geholt.  
- **ID (Instruction Decode):** Die Instruktion wird dekodiert, Register werden gelesen.  
- **OF (Operand Fetch):** Operanden werden vorbereitet.  
- **IE (Instruction Execute):** Die eigentliche Operation (z. B. Addition) wird ausgeführt.  
- **OS (Operand Store):** Ergebnis wird in Register oder Speicher zurückgeschrieben.  

Man erkennt, dass während Instruktion 1 noch in der Ausführung ist, bereits weitere 
Instruktionen in früheren Phasen bearbeitet werden. Dadurch steigert die Pipeline den 
Durchsatz erheblich, ohne dass die Taktrate des Prozessors erhöht werden muss.

## Das Plugin‑System in der Praxis
Eine Besonderheit des VexRiscv ist sein **Plugin-System**.
Anstatt alle Funktionen fest in den Prozessor einzubauen, können Entwickler einzelne Bausteine hinzufügen oder weglassen.  

Beispiel:  
- Für ein sehr kleines FPGA kann ein minimaler Prozessor ohne Cache oder Multiplikationseinheit erzeugt werden.  
- Für größere Systeme kann man zusätzliche Plugins einfügen, etwa für Multiplikation, 
Caches oder Debugging. 

Im Folgenden stehen drei realistische Konfigurationen: minimal, „microcontroller-artig“ und eine Variante mit zusätzlichen Rechen-Plugins. Anschließend folgt ein schlanker Top-Level, der die vom Core erzeugten Bus-Schnittstellen nach außen führt.

Übliche Imports:
 ```scala
> import spinal.core._
> import vexriscv._
> import vexriscv.plugin._
 ```
### Minimaler Core (einfachste Konfiguration)

```scala
class VexRiscvMinimal extends Component {
  val cpu = new VexRiscv(
    VexRiscvConfig(
      plugins = List(
        new IBusSimplePlugin(),   // Instruktionsbus, einfache Handshake-Schnittstelle
        new DBusSimplePlugin(),   // Datenbus, einfache Handshake-Schnittstelle
        new DecoderSimplePlugin,  // Instruktionsdecoder
        new RegFilePlugin,        // Registerfile
        new IntAluPlugin          // Ganzzahl-ALU
      )
    )
  )
}
```
Diese Konfiguration eignet sich für sehr kleine FPGAs und Demonstrationen. Sie hat weder
Caches noch CSR‑Funktionen und ist dadurch leicht zu verstehen

In diesem Beispiel wird ein Prozessor mit einem einfachen Instruktionsbus, einem Datenbus, einem Decoder, einem Registerfile und einer arithmetischen Logikeinheit (ALU) erzeugt.

Der VexRiscv zeigt sehr deutlich, wie mächtig SpinalHDL ist. Während klassische HDLs schnell unübersichtlich werden, wenn man modulare und parametrisierbare Designs bauen möchte, bietet SpinalHDL hier große Vorteile. Dass ein kompletter Prozessor mit Scala und SpinalHDL beschrieben werden kann und anschließend als Verilog oder VHDL generiert wird, beweist die Praxistauglichkeit dieser Sprache.

### “MCU”-Profil (etwas umfangreicher)
```scala
class VexRiscvMcu extends Component {
  val cpu = new VexRiscv(
    VexRiscvConfig(
      plugins = List(
        new IBusSimplePlugin(resetVector = 0x00000000L),
        new DBusSimplePlugin(),
        new DecoderSimplePlugin,
        new RegFilePlugin,
        new IntAluPlugin,
        new HazardSimplePlugin,     // einfaches Hazard-Handling in der Pipeline
        new BranchPlugin,           // Sprunglogik
        new CsrPlugin(CsrPluginConfig.small(mtvecInit = 0x00000000L))
      )
    )
  )
}
```
Diese Konfiguration ist bereits deutlich leistungsfähiger.
Mit Hazard-Handling lassen sich Pipeline-Konflikte automatisch auflösen, und mit dem CSR-Plugin (Control and Status Registers) erhält der Prozessor die Basis für Betriebssystem-ähnliche Software.
Das ist die Konfiguration, die man in einem kleinen SoC (z. B. mit UART, Timer und On-Chip-RAM) nutzen würde.

### Variante mit zusätzlichen Recheneinheiten
```
class VexRiscvWithMulDiv extends Component {
  val cpu = new VexRiscv(
    VexRiscvConfig(
      plugins = List(
        new IBusSimplePlugin(resetVector = 0x00000000L),
        new DBusSimplePlugin(),
        new DecoderSimplePlugin,
        new RegFilePlugin,
        new IntAluPlugin,
        // Zusätzliche Recheneinheiten:
        new MulPlugin,              // Multiplikation
        new DivPlugin,              // Division
        new BranchPlugin,
        new HazardSimplePlugin
      )
    )
  )
}
```
Mit dieser Konfiguration erhält der Prozessor Unterstützung für Multiplikation und Division.
Das ist besonders nützlich, wenn man Anwendungen ausführen möchte, die stark auf mathematische Operationen angewiesen sind (z. B. Signalverarbeitung oder Kryptographie).

### Top-Level: Bus aus dem Core herausführen
Die Bus-Schnittstellen der Plugins lassen sich einfach nach außen führen.
So kann man den Prozessor mit Speicher, Peripherie oder einem SoC-Framework verbinden.
```
class VexRiscvTop extends Component {
  val io = new Bundle {
    val iBus = master(IBusSimpleBus())   // Instruktionsbus
    val dBus = master(DBusSimpleBus())   // Datenbus
  }

  val core = new VexRiscv(
    VexRiscvConfig(
      plugins = List(
        new IBusSimplePlugin(resetVector = 0x00000000L),
        new DBusSimplePlugin(),
        new DecoderSimplePlugin,
        new RegFilePlugin,
        new IntAluPlugin
      )
    )
  )

  // Plugins im Core finden und Interfaces verbinden
  private val iBusP = core.plugins.collectFirst { case p: IBusSimplePlugin => p }.get
  private val dBusP = core.plugins.collectFirst { case p: DBusSimplePlugin => p }.get

  io.iBus <> iBusP.iBus
  io.dBus <> dBusP.dBus
}
```
Damit steht ein Prozessor-Top-Level zur Verfügung, der wie eine normale Komponente
in andere Designs integriert werden kann.

### Verilog generieren
```
object VexRiscvTopVerilog {
  def main(args: Array[String]): Unit = {
    SpinalVerilog(new VexRiscvTop)
  }
}
```
Dieser kleine Generator erzeugt aus dem SpinalHDL-Design den entsprechenden Verilog-Code,
der in gängigen FPGA-Toolchains weiterverwendet werden kann.

## Fazit
Die drei Konfigurationen zeigen, wie man mit wenigen Zeilen Code von einem sehr kleinen 
Core zu einem funktionsreicheren Design gelangt. Das Plugin-System ist dabei der Schlüssel: 
Es erlaubt, gezielt Fähigkeiten hinzuzufügen und gleichzeitig die Kontrolle über 
Ressourcenverbrauch und Komplexität zu behalten.
Der VexRiscv verdeutlicht damit, dass SpinalHDL nicht nur für einfache Module geeignet ist, 
sondern auch für komplette Prozessorarchitekturen praxistauglich eingesetzt werden kann.

# Zusammenfassung und Ausblick

In dieser Dokumentation wurden die Grundlagen von SpinalHDL vorgestellt. 
Wir haben gesehen, wie sich einfache Module wie Zähler, PWM-Generatoren oder Comparatoren 
in wenigen Zeilen Code beschreiben lassen. Dabei wurde deutlich, dass SpinalHDL dank 
starker Typisierung, klarer Syntax und nahtloser Integration von Simulation und Test 
einen deutlichen Vorteil gegenüber klassischen HDLs bietet.

Am Beispiel des VexRiscv-Prozessors wurde gezeigt, dass SpinalHDL auch für 
hochkomplexe Designs geeignet ist. Die modulare Architektur und das Plugin-System 
ermöglichen es, Prozessorvarianten flexibel zu konfigurieren von sehr kleinen 
Cores bis hin zu vollwertigen Systemen mit Multiplikation, Division und CSR-Unterstützung. 
Damit wird sichtbar, wie SpinalHDL vom Prototyping bis zur realen SoC-Entwicklung 
eingesetzt werden kann.

Ein möglicher Ausblick ist die weitere Erforschung von **skalierbaren SoC-Architekturen**, 
die mit SpinalHDL entworfen werden. Durch die Kombination mit Open-Source-Projekten 
wie LiteX oder der Integration in FPGA-Toolchains können Entwickler komplette 
Systeme entwerfen, die von der einfachen Steuerlogik bis hin zu 
leistungsfähigen RISC-V-Prozessoren reichen.  

SpinalHDL ist damit nicht nur ein Werkzeug für den Einstieg, 
sondern eine ernstzunehmende Alternative zu VHDL und Verilog, 
die sich in Zukunft noch stärker in der Hardwareentwicklung etablieren dürfte.
