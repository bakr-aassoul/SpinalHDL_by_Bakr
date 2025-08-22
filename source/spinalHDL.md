# Einleitung

## Ziele dieser Dokumentation
Diese Dokumentation verfolgt das Ziel, einen leicht verständlichen Einstieg in SpinalHDL zu 
geben und die wichtigsten Grundlagen systematisch aufzubereiten. Neben der 
theoretischen Einführung werden praxisnahe Beispiele vorgestellt, die den gesamten 
Entwicklungsworkflow abdecken. Dazu gehören die Komponentenbeschreibung, die 
Simulation und schließlich die Generierung von Verilog- oder VHDL-Code. Auf diese Weise 
soll ein Fundament geschaffen werden, auf dem Leserinnen und Leser sowohl kleine 
Experimente als auch größere Projekte selbstständig entwickeln können. Darüber hinaus 
wird ein Ausblick auf komplexere Designs wie den VexRiscv-Prozessor gegeben, um die 
Skalierbarkeit von SpinalHDL aufzuzeigen.

## Motivation
SpinalHDL ist eine moderne Hardwarebeschreibungssprache, die als Domain-Specific 
Language (DSL) in Scala implementiert ist. Sie bietet eine typensichere, modulare und 
ausdrucksstarke Möglichkeit, digitale Schaltungen zu entwerfen, und generiert daraus 
synthetisierbaren Verilog- oder VHDL-Code für etablierte FPGA- und ASIC-Toolchains.  

Das zentrale Anliegen von SpinalHDL ist es, die Entwicklung digitaler Hardware einfacher, 
produktiver und zugleich zuverlässiger zu gestalten. Anstelle der starren und oft 
fehleranfälligen Ansätze klassischer HDLs wie VHDL oder Verilog bietet SpinalHDL eine 
moderne Syntax, die es Entwicklern erlaubt, Schaltungen klar, modular und 
wiederverwendbar zu beschreiben. Durch die Integration bewährter 
Softwareentwicklungsprinzipien (etwa Unit-Tests, parametrisierbare Module und 
IDE-Unterstützung) entsteht eine Arbeitsweise, die sowohl präzise als auch effizient ist. 
Gleichzeitig bleibt die volle Kompatibilität zur etablierten FPGA- und ASIC-Toolchain 
erhalten, da SpinalHDL automatisch synthetisierbaren Verilog- oder VHDL-Code erzeugt. 
Damit schlägt SpinalHDL eine Brücke zwischen den Methoden moderner 
Softwareentwicklung und der Zuverlässigkeit klassischer Hardwarebeschreibung.


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

```scala
when(cond) {
  // true-Zweig
} elsewhen(otherCond) {
  // anderer Zweig
} otherwise {
  // fallback-Zweig
}
```

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
In der Praxis hat sich **IntelliJ IDEA** mit installiertem Scala-Plugin bewährt. Damit stehen Funktionen wie Code-Vervollständigung, Syntaxhervorhebung und Refactoring zur Verfügung, die die Entwicklung deutlich vereinfachen.
Als Build-Tool wird **sbt (Scala Build Tool)** eingesetzt. Es verwaltet die Abhängigkeiten, kompiliert den Quellcode und führt Programme aus. Dadurch lässt sich der gesamte Entwicklungsprozess strukturiert und reproduzierbar abwickeln.

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
Da SpinalHDL in Scala integriert ist, können Schaltungen direkt in der Java Virtual Machine simuliert werden. Mit Hilfsmitteln wie `SimConfig` und `ScalaTest` lassen sich präzise und wiederholbare Testfälle erstellen. Dies ermöglicht eine enge Verzahnung von Entwicklung, Simulation und Verifikation und erleichtert das Debugging erheblich.

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
Im Folgenden werden einige typische Praxisbeispiele vorgestellt, die den Einsatz von SpinalHDL verdeutlichen. Jedes Beispiel enthält die Beschreibung des Moduls, eine Testbench zur Simulation sowie die Möglichkeit, eine Verilog-Datei zu generieren. Auf diese Weise wird der komplette Ablauf von der Modellierung über die Verifikation bis 
zur Codegenerierung sichtbar.

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
│   └── test/scala/
│       └── ComparatorSim.scala     // Testbench
└── README.md
```

**Aufbau des Moduls**

```scala
class Comparator(width: Int) extends Component {
  val io = new Bundle {
    val a      = in UInt(width bits)
    val b      = in UInt(width bits)
    val equal  = out Bool()
    val greater = out Bool()
    val less   = out Bool()
  }

  io.equal   := io.a === io.b
  io.greater := io.a > io.b
  io.less    := io.a < io.b
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
import spinal.sim._
import spinal.core.sim._

object ComparatorSim {
  def main(args: Array[String]): Unit = {
    SimConfig.withWave.compile(new Comparator(4)).doSim { dut =>
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
    SpinalVerilog(new Comparator(4))
  }
}
```


**Verwendung**

```bash
sbt compile
sbt "runMain ComparatorSim"
sbt "runMain ComparatorVerilog"
```

Ergebnis: Die Datei `Comparator.v` wird generiert, und die Testbench prüft die Vergleichsfunktionen.

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
│   └── test/scala/
│       └── CounterSim.scala     // Testbench
└── README.md
```

**Aufbau des Moduls**

```scala
class Counter(width: Int) extends Component {
  val io = new Bundle {
    val enable = in Bool()
    val reset  = in Bool()
    val value  = out UInt(width bits)
  }

  val count = Reg(UInt(width bits)) init(0)

  when(io.reset) {
    count := 0
  } .elsewhen(io.enable) {
    count := count + 1
  }

  io.value := count
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
    SimConfig.withWave.compile(new Counter(4)).doSim { dut =>
      dut.clockDomain.forkStimulus(10)

      dut.io.reset #= true
      dut.io.enable #= false
      dut.clockDomain.waitSampling()

      dut.io.reset #= false
      dut.io.enable #= true

      for (i <- 0 until 5) {
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
  def main(args: Array[String]): Unit = {
    SpinalVerilog(new Counter(4))
  }
}
```
**Verwendung**

```bash
sbt compile
sbt "runMain CounterSim"
sbt "runMain CounterVerilog"
```

**Ergebnis:**
Die Datei `Counter.v` wird generiert. In der Simulation zählt der Wert bei `enable = true` hoch.



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
│   └── test/scala/
│       └── ClockDividerSim.scala     // Testbench
└── README.md
```

**Aufbau des Moduls**

```scala
class ClockDivider(divisorWidth: Int) extends Component {
  val io = new Bundle {
    val clkOut = out Bool()
  }

  val counter = Reg(UInt(divisorWidth bits)) init(0)
  counter := counter + 1
  io.clkOut := counter.msb
}
```
**Was macht das Modul?**

- `counter`: Zählt kontinuierlich bei jedem Takt.
- `msb`: Der höchste Bitwert des Zählers (Most Significant Bit) wird als geteilter Takt ausgegeben.
- **Beispiel**: Bei `divisorWidth = 8` ergibt sich ein Teiler von 256 (halbe Periode = 128 Takte).


**Testbench: `ClockDividerSim.scala`**
```scala
import spinal.core._
import spinal.sim._
import spinal.core.sim._

object ClockDividerSim {
  def main(args: Array[String]): Unit = {
    SimConfig.withWave.compile(new ClockDivider(8)).doSim { dut =>
      dut.clockDomain.forkStimulus(10)

      for (i <- 0 until 300) {
        dut.clockDomain.waitSampling()
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
    SpinalVerilog(new ClockDivider(8))
  }
}
```

**Verwendung**

```bash
sbt compile
sbt "runMain ClockDividerSim"
sbt "runMain ClockDividerVerilog"
```

Das erzeugt:
- `ClockDivider.v`: die Verilog-Datei
- und zeigt die Simulation mit `clkOut`, der etwa alle 128 Takte wechselt.


## PWM

Dies ist ein einfaches SpinalHDL-Projekt, das ein parametrierbares PWM-Modul (Pulsweitenmodulation) implementiert. Es enthält:

- eine Hardwarebeschreibung (`Pwm.scala`)
- eine Testbench (`PwmSim.scala`)
- eine Verilog-Ausgabe (`PwmVerilog.scala`)
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
│   │       ├── Pwm.scala           ← [1] PWM-Modul
│   │       └── PwmVerilog.scala    ← [3] Verilog-Ausgabe
│   └── test/
│       └── scala/
│           └── PwmSim.scala        ← [2] Simulation
└── README.md
```

**Erklärung des PWM-Moduls**

Das PWM-Modul erzeugt ein Signal, das schnell zwischen **an (1)** und **aus (0)** wechselt.  
Wie lange das Signal „an“ bleibt, hängt vom **Duty-Cycle** ab – einem Eingabewert, der angibt, wie viel Prozent der Zeit das Signal „an“ sein soll.

**Aufbau des Moduls**

```scala
class Pwm(width: Int) extends Component {
  val io = new Bundle {
    val enable = in Bool()
    val duty   = in UInt(width bits)
    val pwmOut = out Bool()
  }

  val counter = Reg(UInt(width bits)) init(0)
  counter := counter + 1
  io.pwmOut := io.enable && (counter < io.duty)
}
```

**Was macht das Modul?**

- `width`: Gibt an, wie genau das PWM-Signal sein soll (z. B. 8 Bit → Werte von 0 bis 255).
- `enable`: Schaltet das PWM-Signal ein oder aus.
- `duty`: Bestimmt, wie lange das Signal „an“ sein soll (je höher der Wert, desto länger).
- `counter`: Zählt von 0 bis zum Maximalwert und beginnt dann wieder von vorn.
- `pwmOut`: Wird „an“, solange `counter < duty`.

###  Beispiel (bei 8 Bit Auflösung)

- `duty = 0` → Signal ist immer aus
- `duty = 128` → Signal ist 50 % der Zeit an
- `duty = 255` → Signal ist immer an

Das Modul vergleicht einen Zähler mit einem Zielwert (`duty`).  
Solange der Zähler kleiner ist, ist das Signal **an**  danach **aus**.  
Dieser Zyklus wiederholt sich ständig.

**[1] `src/main/scala/Pwm.scala` (Code wie oben)**

Siehe oben unter „Aufbau des Moduls“.

**[2] `src/test/scala/PwmSim.scala`**

```scala
import spinal.core._
import spinal.sim._
import spinal.core.sim._

object PwmSim {
  def main(args: Array[String]): Unit = {
    SimConfig
      .withWave
      .compile(new Pwm(8)) // 8-Bit PWM
      .doSim { dut =>
        dut.clockDomain.forkStimulus(10)

        dut.io.enable #= true
        dut.io.duty   #= 128 // 50% Duty Cycle

        for (cycle <- 0 until 300) {
          dut.clockDomain.waitSampling()
        }

        simSuccess()
      }
  }
}
```
**`[3]PwmVerilog.scala`**

```scala
import spinal.core._

object PwmVerilog {
  def main(args: Array[String]): Unit = {
    SpinalVerilog(new Pwm(8))
  }
}
```



**`build.sbt`**

```scala
name := "pwm-spinalhdl"

version := "0.1"

scalaVersion := "2.13.12"

libraryDependencies ++= Seq(
  "com.github.spinalhdl" %% "spinalhdl-core" % "1.9.1",
  "com.github.spinalhdl" %% "spinalhdl-sim"  % "1.9.1" % Test
)
```



**Projekt kompilieren und starten**



```bash
sbt compile
```

```bash
sbt "runMain PwmVerilog"
```

```bash
sbt "runMain PwmSim"
```


**Ergebnis**

- Wir erhalten ein synthetisierbares PWM-Modul  
- Wir können das Verhalten direkt simulieren  
- Der generierte Verilog-Code (`Pwm.v`) ist für FPGA/ASIC verwendbar

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
<img width="602" height="377" alt="Screenshot 2025-08-22 at 14 09 24" src="https://github.com/user-attachments/assets/91404905-f756-4b6a-950c-4e9791b61e3d" />

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
ermöglichen es, Prozessorvarianten flexibel zu konfigurieren – von sehr kleinen 
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
